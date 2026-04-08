# -*- coding: utf-8 -*-
"""
recorder — ULTRA
- record_once on enable if autostart and seconds>0
- Queue: .rec files -> record N seconds, write WAV to dir
"""

from typing import Dict, Any, Optional, Callable
import os, json, threading, time, traceback

CONFIG: Dict[str, Any] = {}
_ENABLED = False
_THREAD: Optional[threading.Thread] = None
_STOP = threading.Event()

def _config_dir() -> str:
    return os.environ.get("VTP_CONFIG_DIR", "config")

def _config_path(mod_id: str) -> str:
    return os.path.join(_config_dir(), f"{mod_id}.json")

def _queue_dir(mod_id: str) -> str:
    base = os.environ.get("VTP_QUEUE_DIR", os.path.join("runtime", "queue"))
    return os.path.join(base, mod_id)

def _load_config(mod_id: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    cfg = dict(defaults or {})
    try:
        with open(_config_path(mod_id), "r", encoding="utf-8") as f:
            file_cfg = json.load(f)
            if isinstance(file_cfg, dict):
                cfg.update(file_cfg)
    except Exception:
        pass
    # env overrides like VTP_<ID>_KEY=VALUE (JSON if parseable)
    pfx = f"VTP_{mod_id.upper()}_"
    for k, v in os.environ.items():
        if not k.startswith(pfx): continue
        key = k[len(pfx):].lower()
        try: cfg[key] = json.loads(v)
        except Exception: cfg[key] = v
    return cfg

def _ensure_dirs(mod_id: str):
    os.makedirs(_config_dir(), exist_ok=True)
    os.makedirs(_queue_dir(mod_id), exist_ok=True)

def _worker_loop(mod_id: str, fn: Callable[[str], None], ext_list):
    qdir = _queue_dir(mod_id)
    while not _STOP.is_set():
        try:
            files = [f for f in os.listdir(qdir) if any(f.lower().endswith(ext) for ext in ext_list)]
            files.sort()
            for name in files:
                if _STOP.is_set(): break
                path = os.path.join(qdir, name)
                try:
                    fn(path)
                    # mark done
                    os.rename(path, path + ".done")
                except Exception as e:
                    with open(path + ".err.txt", "w", encoding="utf-8") as err:
                        err.write(str(e) + "\n" + traceback.format_exc())
        except Exception:
            pass
        _STOP.wait(0.5)


DEFAULTS = {"enabled": False, "dir":"records", "seconds":2, "samplerate": 16000, "channels":1, "autostart": False}
CONFIG = _load_config("recorder", DEFAULTS)

def _have():
    try:
        import sounddevice, soundfile  # type: ignore
        return True
    except Exception:
        return False

def _do_record(seconds: int, out_path: str):
    import sounddevice as sd, soundfile as sf
    fs = int(CONFIG.get("samplerate") or 16000); ch = int(CONFIG.get("channels") or 1)
    data = sd.rec(int(seconds*fs), samplerate=fs, channels=ch, dtype='int16')
    sd.wait(); sf.write(out_path, data, fs)

def _job(path: str):
    seconds = int(open(path, "r", encoding="utf-8").read().strip() or CONFIG.get("seconds",2))
    os.makedirs(CONFIG.get("dir","records"), exist_ok=True)
    name = os.path.join(CONFIG.get("dir","records"), f"rec_{int(time.time())}.wav")
    _do_record(seconds, name)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = bool(CONFIG.get("enabled", True)); _ensure_dirs("recorder")
    if CONFIG.get("autostart") and _THREAD is None and _have():
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("recorder", _job, [".rec"]), daemon=True); _THREAD.start()
        if CONFIG.get("seconds",0)>0:
            tmp = os.path.join(_queue_dir("recorder"), "_once.rec")
            open(tmp, "w", encoding="utf-8").write(str(CONFIG.get("seconds",2)))
    return {"ok": True, "enabled": _ENABLED}
def health():
    if not _have(): return {"ok": False, "module":"recorder", "need":"pip install sounddevice soundfile"}
    return {"ok": True, "module":"recorder"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("recorder", configure, enable, health)
except Exception: pass
