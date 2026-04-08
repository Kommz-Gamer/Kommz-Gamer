# -*- coding: utf-8 -*-
"""
Module: util_logging
VTP PRO base — loads config from FS, robust health, safe defaults.
Generated: 2025-09-06

Config sources (merged left→right):
  1) Module defaults in code
  2) File: ./config/util_logging.json
  3) Env:  VTP_UTIL_LOGGING_* (JSON for complex fields)
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
  "level": "info",
  "file": "logs/app.log",
  "rotate": "10MB"
}
CONFIG = _load_config('util_logging', DEFAULTS, 'UTIL_LOGGING')

import logging, logging.handlers, os
def _level(lvl: str) -> int:
    return {"debug": logging.DEBUG, "info": logging.INFO, "warn": logging.WARN, "error": logging.ERROR}.get((CONFIG.get("level","info")).lower(), logging.INFO)
def configure(cfg: Dict[str, Any]) -> Dict[str, Any]:
    global CONFIG; CONFIG = _merge(CONFIG, cfg or {})
    lvl = _level(CONFIG.get("level", "info"))
    os.makedirs(os.path.dirname(CONFIG.get("file","logs/app.log")), exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(CONFIG.get("file","logs/app.log"), maxBytes=10*1024*1024, backupCount=3)
    logging.basicConfig(level=lvl, handlers=[handler], format="%(asctime)s %(levelname)s %(name)s — %(message)s")
    return {"ok": True, "applied": CONFIG}
def enable() -> Dict[str, Any]:
    global _ENABLED; _ENABLED = True; logging.getLogger("util_logging").info("logging enabled"); return {"ok": True, "enabled": True}
def health() -> Dict[str, Any]:
    try: logging.getLogger("util_logging").debug("health"); return {"ok": True, "module": "util_logging"}
    except Exception as e: return {"ok": False, "error": str(e), "module": "util_logging"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("util_logging", configure, enable, health)
except Exception:
    pass
