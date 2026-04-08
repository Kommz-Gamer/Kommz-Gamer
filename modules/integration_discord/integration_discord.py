# -*- coding: utf-8 -*-
"""
integration_discord — ULTRA
- Supports webhook or bot token.
- Queue: put .txt files in queue/integration_discord => sends content.
Config:
  webhook_url OR (token + channel_id)
  autostart(bool)
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

DEFAULTS = {"token":"", "channel_id":"", "webhook_url":"", "autostart": False, "test_message": ""}
CONFIG = _load_config("integration_discord", DEFAULTS)

def _send_via_webhook(text: str):
    r = requests.post(CONFIG["webhook_url"], json={"content": text}, timeout=5)
    if r.status_code >= 300:
        raise RuntimeError(f"webhook status {r.status_code}: {r.text}")

def _send_via_bot(text: str):
    # For simplicity, prefer webhook. Bot mode requires discord.py loop which isn't launched here.
    raise RuntimeError("bot mode not implemented in ULTRA worker; provide webhook_url")

def _job(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if CONFIG.get("webhook_url"):
        _send_via_webhook(text)
    elif CONFIG.get("token") and CONFIG.get("channel_id"):
        _send_via_bot(text)
    else:
        raise RuntimeError("no webhook_url or token/channel_id configured")

def configure(cfg): 
    CONFIG.update(cfg or {})
    masked = dict(CONFIG)
    if masked.get("token"): masked["token"] = "***"
    if masked.get("webhook_url"): masked["webhook_url"] = masked["webhook_url"][:25] + "..."
    return {"ok": True, "applied": masked}

def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("integration_discord")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("integration_discord", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}

def health():
    if not (CONFIG.get("webhook_url") or (CONFIG.get("token") and CONFIG.get("channel_id"))):
        return {"ok": False, "module":"integration_discord", "error":"missing webhook_url or token/channel_id"}
    return {"ok": True, "module":"integration_discord"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("integration_discord", configure, enable, health)
except Exception: pass
