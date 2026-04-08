# -*- coding: utf-8 -*-
"""
dedupe_debounce — EXTRA ULTRA
- Supprime répétitions rapprochées. .txt -> .pass.txt si nouveauté.
Config: {"window_s": 2.0}
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

import time, hashlib

DEFAULTS = {"window_s": 2.0, "autostart": False}
CONFIG = _load_config("dedupe_debounce", DEFAULTS)
_LAST = {"hash": None, "ts": 0.0}

def _job(path: str):
    global _LAST
    txt = open(path, "r", encoding="utf-8").read().strip()
    h = hashlib.sha1(txt.encode("utf-8")).hexdigest()
    now = time.time()
    if _LAST["hash"] == h and (now - _LAST["ts"]) < float(CONFIG.get("window_s",2.0)):
        # drop
        open(path + ".drop", "w").write("dropped")
        return
    _LAST = {"hash": h, "ts": now}
    with open(path + ".pass.txt", "w", encoding="utf-8") as f:
        f.write(txt)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("dedupe_debounce")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("dedupe_debounce", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health(): return {"ok": True, "module":"dedupe_debounce"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("dedupe_debounce", configure, enable, health)
except Exception: pass
