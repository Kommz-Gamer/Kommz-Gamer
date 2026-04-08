# -*- coding: utf-8 -*-
"""
Module: util_sync
VTP PRO base — loads config from FS, robust health, safe defaults.
Generated: 2025-09-06

Config sources (merged left→right):
  1) Module defaults in code
  2) File: ./config/util_sync.json
  3) Env:  VTP_UTIL_SYNC_* (JSON for complex fields)
"""

from typing import Dict, Any
import os, json

CONFIG: Dict[str, Any] = {}
_ENABLED = False

def _config_dir() -> str:
    return os.environ.get("VTP_CONFIG_DIR", "config")

def _config_path(mod_id: str) -> str:
    return os.path.join(_config_dir(), f"{mod_id}.json")

def _env_overrides(prefix: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    pfx = f"VTP_{prefix}_"
    for k, v in os.environ.items():
        if not k.startswith(pfx): continue
        key = k[len(pfx):].lower()
        try:
            out[key] = json.loads(v)
        except Exception:
            out[key] = v
    return out

def _merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    z = dict(a or {})
    z.update(b or {})
    return z

def _load_config(mod_id: str, defaults: Dict[str, Any], env_prefix: str) -> Dict[str, Any]:
    cfg = dict(defaults or {})
    try:
        with open(_config_path(mod_id), "r", encoding="utf-8") as f:
            file_cfg = json.load(f)
            if isinstance(file_cfg, dict):
                cfg = _merge(cfg, file_cfg)
    except Exception:
        pass
    env_cfg = _env_overrides(env_prefix)
    cfg = _merge(cfg, env_cfg)
    return cfg

DEFAULTS = {
  "enabled": true,
  "interval_ms": 2000,
  "url": "http://127.0.0.1:8770/api/track/stats2"
}
CONFIG = _load_config('util_sync', DEFAULTS, 'UTIL_SYNC')

import threading, time
def _have_lib():
    try: import requests  # type: ignore; return True
    except Exception: return False
_THREAD=None; _STOP=threading.Event()
def _loop():
    import logging, requests
    log = logging.getLogger("util_sync")
    while not _STOP.is_set():
        try:
            r = requests.get(CONFIG.get("url","http://127.0.0.1:8770/api/track/stats2"), timeout=2)
            log.debug("sync %s -> %s", CONFIG.get("url"), r.status_code)
        except Exception as e:
            log.debug("sync fail: %s", e)
        _STOP.wait((CONFIG.get("interval_ms") or 2000)/1000.0)
def configure(cfg: Dict[str, Any]) -> Dict[str, Any]:
    global CONFIG; CONFIG = _merge(CONFIG, cfg or {}); return {"ok": True, "applied": CONFIG}
def enable() -> Dict[str, Any]:
    global _ENABLED, _THREAD
    if _ENABLED: return {"ok": True, "enabled": True}
    _ENABLED = True; _STOP.clear()
    _THREAD = threading.Thread(target=_loop, daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health() -> Dict[str, Any]:
    if not _have_lib(): return {"ok": False, "module": "util_sync", "need": "pip install requests"}
    return {"ok": True, "module": "util_sync"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("util_sync", configure, enable, health)
except Exception:
    pass
