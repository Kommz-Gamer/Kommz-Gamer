# -*- coding: utf-8 -*-
"""
audio_vad — ULTRA
- Health: verifies webrtcvad.
- Worker (if autostart): watch queue/audio_vad for .wav, writes segments JSON sidecar.
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

import wave

DEFAULTS = {"threshold": 0.5, "min_speech_ms": 120, "autostart": False}
CONFIG = _load_config("audio_vad", DEFAULTS)
try:
    import webrtcvad
    _HAVE = True
except Exception:
    _HAVE = False

def _analyze_wav(path: str):
    if not _HAVE: raise RuntimeError("webrtcvad not installed")
    with wave.open(path, "rb") as wf:
        nch, sampw, rate, nframes, _, _ = wf.getparams()
        if nch != 1 or sampw != 2:
            raise RuntimeError("expect mono 16-bit PCM")
        pcm = wf.readframes(nframes)
    vad = webrtcvad.Vad(2)
    frame_ms = 30
    frame_len = int(rate * frame_ms / 1000) * 2  # 2 bytes per sample
    segments = []
    t = 0.0
    for i in range(0, len(pcm), frame_len):
        chunk = pcm[i:i+frame_len]
        if len(chunk) < frame_len: break
        is_speech = vad.is_speech(chunk, rate)
        segments.append({"t_ms": int(t*1000), "speech": bool(is_speech)})
        t += frame_ms/1000
    with open(path + ".vad.json", "w", encoding="utf-8") as f:
        json.dump({"rate": rate, "frame_ms": frame_ms, "segments": segments}, f, indent=2)

def configure(cfg: Dict[str, Any]) -> Dict[str, Any]:
    global CONFIG; CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}

def enable() -> Dict[str, Any]:
    global _ENABLED, _THREAD
    _ENABLED = True
    _ensure_dirs("audio_vad")
    if CONFIG.get("autostart") and _HAVE and _THREAD is None:
        _STOP.clear()
        _THREAD = threading.Thread(target=_worker_loop, args=("audio_vad", _analyze_wav, [".wav"]), daemon=True)
        _THREAD.start()
    return {"ok": True, "enabled": _ENABLED}

def health() -> Dict[str, Any]:
    if not _HAVE: return {"ok": False, "module":"audio_vad", "need":"pip install webrtcvad"}
    return {"ok": True, "module":"audio_vad"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("audio_vad", configure, enable, health)
except Exception: pass
