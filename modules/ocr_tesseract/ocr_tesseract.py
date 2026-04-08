# -*- coding: utf-8 -*-
"""
ocr_tesseract — EXTRA ULTRA
- Dépose une image dans runtime/queue/ocr_tesseract (png/jpg/bmp) -> .txt
- Nécessite: Tesseract installé + pytesseract + Pillow.
Config:
  tesseract_cmd: chemin vers l'exécutable (Windows ex: "C:/Program Files/Tesseract-OCR/tesseract.exe")
  lang: "eng", "fra", "eng+fra", ...
  psm, oem: options avancées (facultatif)
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

from PIL import Image

DEFAULTS = {"tesseract_cmd":"", "lang":"eng", "psm": 6, "oem": 3, "autostart": False}
CONFIG = _load_config("ocr_tesseract", DEFAULTS)

def _ensure_tess():
    try:
        import pytesseract  # type: ignore
    except Exception:
        return False, "pip install pytesseract pillow"
    if CONFIG.get("tesseract_cmd"):
        try:
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = CONFIG["tesseract_cmd"]
        except Exception as e:
            return False, str(e)
    return True, ""

def _ocr(path: str) -> str:
    import pytesseract  # type: ignore
    img = Image.open(path)
    cfg = ""
    if CONFIG.get("psm") is not None:
        cfg += f" --psm {int(CONFIG['psm'])}"
    if CONFIG.get("oem") is not None:
        cfg += f" --oem {int(CONFIG['oem'])}"
    lang = CONFIG.get("lang","eng")
    return pytesseract.image_to_string(img, lang=lang, config=cfg or None)

def _job(path: str):
    ok, why = _ensure_tess()
    if not ok: raise RuntimeError(why)
    txt = _ocr(path)
    with open(path + ".txt", "w", encoding="utf-8") as f:
        f.write(txt.strip())

def configure(cfg): CONFIG.update(cfg or {}); return {"ok": True, "applied": CONFIG}
def enable():
    global _ENABLED, _THREAD
    _ENABLED = True; _ensure_dirs("ocr_tesseract")
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear(); _THREAD = threading.Thread(target=_worker_loop, args=("ocr_tesseract", _job, [".png",".jpg",".jpeg",".bmp"]), daemon=True); _THREAD.start()
    return {"ok": True, "enabled": True}
def health():
    ok, why = _ensure_tess()
    return {"ok": ok, "module":"ocr_tesseract", "hint": (why or None)}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("ocr_tesseract", configure, enable, health)
except Exception: pass
