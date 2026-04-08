# -*- coding: utf-8 -*-
"""
glossary_rewrite — EXTRA ULTRA
- Remplace termes selon un glossaire (sensible à la casse optionnel).
- .txt -> .gloss.txt
Config: {"map": {"Raze": "Raze (Agent)"}, "case_sensitive": false}
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

import re

DEFAULTS = {"map": {}, "case_sensitive": False, "autostart": False}
CONFIG = _load_config("glossary_rewrite", DEFAULTS)

def _apply(text: str) -> str:
    m = CONFIG.get("map") or {}
    if not m: return text
    flags = 0 if CONFIG.get("case_sensitive") else re.IGNORECASE
    # Replace longest keys first to avoid partial overlap issues
    for k in sorted(m.keys(), key=lambda x: len(x), reverse=True):
        try:
            text = re.sub(re.escape(k), str(m[k]), text, flags=flags)
        except Exception:
            pass
    return text

def _job(path: str):
    txt = open(path, "r", encoding="utf-8").read()
    out = _apply(txt)
    with open(path + ".gloss.txt", "w", encoding="utf-8") as f:
        f.write(out)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("glossary_rewrite")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("glossary_rewrite", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health(): return {"ok": True, "module":"glossary_rewrite"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("glossary_rewrite", configure, enable, health)
except Exception: pass
