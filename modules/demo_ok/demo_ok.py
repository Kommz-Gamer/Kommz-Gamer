# -*- coding: utf-8 -*-
"""
demo_ok — ULTRA
- Always healthy. Writes a hello file if autostart.
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


DEFAULTS = {"autostart": False}
CONFIG = _load_config("demo_ok", DEFAULTS)

def _job(_): 
    with open(os.path.join(_queue_dir("demo_ok"), "hello.txt"), "w", encoding="utf-8") as f:
        f.write("demo_ok running")

def configure(cfg): 
    CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}

def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("demo_ok")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("demo_ok", _job, [".tick"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}

def health(): 
    return {"ok": True, "module":"demo_ok"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("demo_ok", configure, enable, health)
except Exception: pass
