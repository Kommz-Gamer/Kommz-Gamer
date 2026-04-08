# -*- coding: utf-8 -*-
"""
mt_google — ULTRA
- Queue: .txt => writes .mt_google.txt
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

import requests

DEFAULTS = {"source": "auto", "target": "en", "autostart": False, "api_key":"", "project":"", "location":"global"}
CONFIG = _load_config("mt_google", DEFAULTS)

def _translate(text: str) -> str:
    key = CONFIG.get("api_key")
    if not key: raise RuntimeError("missing api_key")
    url = f"https://translation.googleapis.com/language/translate/v2?key={key}"
    data = {"q": text, "target": CONFIG.get("target","en")}
    if CONFIG.get("source") and CONFIG["source"]!="auto": data["source"]=CONFIG["source"]
    r = requests.post(url, json=data, timeout=15); j = r.json()
    return j["data"]["translations"][0]["translatedText"]

def _job(path: str):
    txt = open(path, "r", encoding="utf-8").read()
    out = _translate(txt)
    with open(path + ".mt_google.txt", "w", encoding="utf-8") as f:
        f.write(out)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("mt_google")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("mt_google", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health(): return {"ok": bool(CONFIG.get("api_key")), "module":"mt_google"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("mt_google", configure, enable, health)
except Exception: pass
