# -*- coding: utf-8 -*-
"""
screen_capture — EXTRA ULTRA
- Capture périodiquement une zone d'écran (pas de hook de jeu).
- Autostart: écrit des PNG dans out_dir toutes interval_ms.
- 'one-shot': déposer un fichier .tick -> capture immédiate.
"""

from typing import Dict, Any, Optional, Callable, List
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

def _worker_loop(mod_id: str, fn, ext_list: List[str]):
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

import time, os

DEFAULTS = {"autostart": False, "interval_ms": 1000, "region": {"left":0,"top":0,"width":640,"height":360}, "out_dir":"captures"}
CONFIG = _load_config("screen_capture", DEFAULTS)

def _have():
    try:
        import mss  # type: ignore
        return True
    except Exception:
        return False

def _capture_once():
    import mss  # type: ignore
    os.makedirs(CONFIG.get("out_dir","captures"), exist_ok=True)
    region = CONFIG.get("region") or {"left":0,"top":0,"width":640,"height":360}
    with mss.mss() as sct:
        img = sct.grab({"left": int(region.get("left",0)), "top": int(region.get("top",0)), "width": int(region.get("width",640)), "height": int(region.get("height",360))})
        # Write PNG
        ts = int(time.time()*1000)
        path = os.path.join(CONFIG.get("out_dir","captures"), f"cap_{ts}.png")
        mss.tools.to_png(img.rgb, img.size, output=path)  # type: ignore
        return path

def _job(path: str):
    _capture_once()

def _loop():
    while not _STOP.is_set():
        try: _capture_once()
        except Exception: pass
        _STOP.wait((CONFIG.get("interval_ms") or 1000)/1000.0)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("screen_capture")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_loop, daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health():
    if not _have(): return {"ok": False, "module":"screen_capture", "need":"pip install mss"}
    return {"ok": True, "module":"screen_capture"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("screen_capture", configure, enable, health)
except Exception: pass
