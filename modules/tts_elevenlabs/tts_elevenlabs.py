# -*- coding: utf-8 -*-
"""
Module: tts_elevenlabs
VTP PRO base — loads config from FS, robust health, safe defaults.
Generated: 2025-09-06

Config sources (merged left→right):
  1) Module defaults in code
  2) File: ./config/tts_elevenlabs.json
  3) Env:  VTP_TTS_ELEVENLABS_* (JSON for complex fields)
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
  "api_key": "",
  "voice_id": "",
  "stability": 0.5
}
CONFIG = _load_config('tts_elevenlabs', DEFAULTS, 'TTS_ELEVENLABS')

def _have_lib():
    try: import requests  # type: ignore; return True
    except Exception: return False
def configure(cfg: Dict[str, Any]) -> Dict[str, Any]:
    global CONFIG; CONFIG = _merge(CONFIG, cfg or {})
    masked = {"api_key": "***" if CONFIG.get("api_key") else ""}; out = dict(CONFIG); out.update(masked)
    return {"ok": True, "applied": out}
def enable() -> Dict[str, Any]:
    global _ENABLED; _ENABLED = bool(CONFIG.get("api_key")); return {"ok": True, "enabled": _ENABLED}
def health() -> Dict[str, Any]:
    if not _have_lib(): return {"ok": False, "module": "tts_elevenlabs", "need": "pip install requests"}
    if not CONFIG.get("api_key"): return {"ok": False, "module": "tts_elevenlabs", "error": "missing api_key"}
    return {"ok": True, "module": "tts_elevenlabs"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("tts_elevenlabs", configure, enable, health)
except Exception:
    pass
