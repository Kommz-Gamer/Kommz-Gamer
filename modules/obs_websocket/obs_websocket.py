# -*- coding: utf-8 -*-
"""
obs_websocket — EXTRA ULTRA
- Dépose .txt -> met à jour la source texte (GDI+ / FreeType) dans OBS.
- Requiert obs-websocket activé (v5). Lib: obsws-python.
Config:
  host, port, password, source_name
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


DEFAULTS = {"host":"127.0.0.1", "port":4455, "password":"", "source_name":"ChatOverlay", "autostart": False}
CONFIG = _load_config("obs_websocket", DEFAULTS)

def _client():
    try:
        import obsws_python as obs  # type: ignore
    except Exception:
        raise RuntimeError("pip install obsws-python")
    return obs.ReqClient(host=CONFIG.get("host","127.0.0.1"), port=int(CONFIG.get("port",4455)), password=CONFIG.get("password",""))

def _set_text(text: str):
    cli = _client()
    # For GDI+ text, the setting key is "text"
    cli.set_input_settings(inputName=CONFIG.get("source_name","ChatOverlay"), inputSettings={"text": text}, overlay=True)

def _job(path: str):
    txt = open(path, "r", encoding="utf-8").read()
    _set_text(txt)

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("obs_websocket")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("obs_websocket", _job, [".txt"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health():
    try:
        _client()
        return {"ok": True, "module":"obs_websocket"}
    except Exception as e:
        return {"ok": False, "module":"obs_websocket", "error": str(e), "hint":"Assure-toi que obs-websocket v5 est actif et que le mot de passe est correct"}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("obs_websocket", configure, enable, health)
except Exception: pass
