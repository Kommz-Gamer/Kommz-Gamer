# -*- coding: utf-8 -*-
"""
tts_edge — ULTRA
- Queue: .txt files -> synthesize with edge-tts -> out_dir/<basename>.mp3
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

def _worker_loop(mod_id: str, fn, ext_list):
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
                    os.rename(path, path + ".done")
                except Exception as e:
                    with open(path + ".err.txt", "w", encoding="utf-8") as err:
                        err.write(str(e) + "\n" + traceback.format_exc())
        except Exception:
            pass
        _STOP.wait(0.5)

DEFAULTS = {"voice":"fr-FR", "rate":1.0, "pitch":0, "out_dir":"tts_out", "autostart": False}
CONFIG = _load_config("tts_edge", DEFAULTS)

def _have_lib():
    try:
        import edge_tts  # type: ignore
        return True
    except Exception:
        return False

def _synthesize(text: str, out_path: str):
    import asyncio, edge_tts  # type: ignore
    # rate: convert multiplier to +/- percentage string
    if float(CONFIG.get("rate",1.0)) == 1.0:
        rate = "+0%"
    else:
        rate_pct = int((float(CONFIG.get("rate",1.0))-1.0)*100)
        sign = "+" if rate_pct >= 0 else ""
        rate = f"{sign}{rate_pct}%"
    pitch_val = int(CONFIG.get("pitch",0))
    pitch = ("+" if pitch_val>=0 else "") + str(pitch_val) + "Hz"
    async def run():
        communicate = edge_tts.Communicate(text, CONFIG.get("voice","fr-FR"), rate=rate, pitch=pitch)
        await communicate.save(out_path)
    asyncio.run(run())

def _job(path: str):
    if not _have_lib(): raise RuntimeError("edge-tts not installed")
    os.makedirs(CONFIG.get("out_dir","tts_out"), exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    out = os.path.join(CONFIG.get("out_dir","tts_out"), base + ".mp3")
    txt = open(path, "r", encoding="utf-8").read()
    _synthesize(txt, out)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("tts_edge")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("tts_edge", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health():
    if not _have_lib(): return {"ok": False, "module":"tts_edge", "need":"pip install edge-tts"}
    return {"ok": True, "module":"tts_edge"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("tts_edge", configure, enable, health)
except Exception: pass
