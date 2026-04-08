# -*- coding: utf-8 -*-
"""
ping — ULTRA
- True TCP connect timing
- Queue: .host files with host:port (port default 443) -> writes .ms
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

import socket, time

DEFAULTS = {"hosts": ["1.1.1.1", "8.8.8.8"], "timeout_ms": 2000} if "ping"=="latency" else {"target":"1.1.1.1", "timeout_ms":2000}
CONFIG = _load_config("ping", DEFAULTS)

def _tcp(host: str, port: int = 443, timeout: float = 2.0):
    t0 = time.time(); s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(timeout)
    try:
        s.connect((host, port)); s.close(); return True, (time.time()-t0)*1000.0
    except Exception:
        return False, -1.0

def _job(path: str):
    q = open(path, "r", encoding="utf-8").read().strip()
    host, _, port = q.partition(":"); port = int(port) if port else 443
    ok, ms = _tcp(host, port, (CONFIG.get("timeout_ms") or 2000)/1000.0)
    with open(path + ".ms", "w", encoding="utf-8") as f:
        f.write(str(round(ms,2)) if ok else "ERR")

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD; _ENABLED = True; _ensure_dirs("ping")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("ping", _job, [".host"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health():
    if "ping"=="latency":
        hosts = CONFIG.get("hosts") or ["1.1.1.1"]
        for h in hosts:
            ok, ms = _tcp(h, 443, (CONFIG.get("timeout_ms") or 2000)/1000.0)
            if ok: return {"ok": True, "module":"ping", "via":"tcp:443", "host":h, "ms": round(ms,2)}
        return {"ok": False, "module":"ping", "error":"no host reachable"}
    else:
        ok, ms = _tcp(CONFIG.get("target") or "1.1.1.1", 443, (CONFIG.get("timeout_ms") or 2000)/1000.0)
        return {"ok": ok, "module":"ping", "ms": round(ms,2) if ms>=0 else None}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("ping", configure, enable, health)
except Exception: pass
