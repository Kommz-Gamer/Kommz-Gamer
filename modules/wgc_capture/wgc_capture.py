# -*- coding: utf-8 -*-
"""
wgc_capture — ULTRA (multi-profiles)
Safe Windows capture using DXGI Desktop Duplication (dxcam) or MSS.
- Multiple game profiles (per-game settings).
- Auto-switch based on foreground process (exe) or title.
- Manual switch by dropping a `.profile` file (content = profile name).
- One-shot capture by dropping a `.tick` file.

Requires:
  pip install dxcam Pillow mss pywin32 psutil
"""
from typing import Dict, Any, Optional, Tuple
import os, json, threading, time, traceback

CONFIG: Dict[str, Any] = {}
_ENABLED = False
_THREAD: Optional[threading.Thread] = None
_STOP = threading.Event()
_ACTIVE_PROFILE = None  # type: Optional[str]

def _config_dir() -> str:
    return os.environ.get("VTP_CONFIG_DIR", "config")

def _config_path(mod_id: str) -> str:
    return os.path.join(_config_dir(), f"{mod_id}.json")

def _queue_dir(mod_id: str) -> str:
    base = os.environ.get("VTP_QUEUE_DIR", os.path.join("runtime", "queue"))
    return os.path.join(base, mod_id)

def _load_config(defaults: Dict[str, Any]) -> Dict[str, Any]:
    mod_id = "wgc_capture"
    cfg = dict(defaults or {})
    try:
        with open(_config_path(mod_id), "r", encoding="utf-8") as f:
            file_cfg = json.load(f)
            if isinstance(file_cfg, dict):
                cfg.update(file_cfg)
    except Exception:
        pass
    pfx = "VTP_WGC_CAPTURE_"
    for k, v in os.environ.items():
        if not k.startswith(pfx): continue
        key = k[len(pfx):].lower()
        try: cfg[key] = json.loads(v)
        except Exception: cfg[key] = v
    return cfg

def _ensure_dirs():
    os.makedirs(_config_dir(), exist_ok=True)
    os.makedirs(_queue_dir("wgc_capture"), exist_ok=True)

DEFAULTS = {
    "autostart": False,
    "backend": "dxcam",     # default backend if profile doesn't override
    "mode": "region",
    "monitor": 0,
    "region": {"left":0,"top":0,"width":800,"height":450},
    "window_title": "VALORANT",
    "window_exe": "",       # optional exe name (e.g., "VALORANT-Win64-Shipping.exe")
    "fps": 20,
    "out_dir": "captures_wgc",
    # Multi-profile support
    "profiles": {},         # name -> dict of same keys (backend/mode/monitor/region/window_title/window_exe/fps/out_dir)
    "active_profile": "",   # name
    "auto_switch": True,    # if true, choose profile by foreground exe/title using auto_map
    "auto_map": {}          # exe_or_title_lower -> profile_name
}
CONFIG = _load_config(DEFAULTS)

def _now_ms():
    return int(time.time() * 1000)

def _png_path(prefix="wgc", out_dir=None):
    out = out_dir or CONFIG.get("out_dir","captures_wgc")
    os.makedirs(out, exist_ok=True)
    ts = _now_ms()
    return os.path.join(out, f"{prefix}_{ts}.png")

def _get_foreground_exe_title() -> Tuple[str, str]:
    exe, title = "", ""
    try:
        import win32gui, win32process  # type: ignore
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd) or ""
            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid:
                    try:
                        import psutil  # type: ignore
                        p = psutil.Process(pid)
                        exe = os.path.basename(p.exe() or "") or (p.name() or "")
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        pass
    return exe, title

def _resolve_profile() -> Dict[str, Any]:
    global _ACTIVE_PROFILE
    profs = CONFIG.get("profiles") or {}
    # Auto-switch logic
    if CONFIG.get("auto_switch"):
        exe, title = _get_foreground_exe_title()
        key_candidates = []
        if exe: key_candidates.append(exe.lower())
        if title: key_candidates.append(title.lower())
        amap = {str(k).lower(): str(v) for k, v in (CONFIG.get("auto_map") or {}).items()}
        for k in key_candidates:
            if k in amap and amap[k] in profs:
                _ACTIVE_PROFILE = amap[k]
                break
    # Fallback to explicitly set active profile
    if not _ACTIVE_PROFILE:
        ap = str(CONFIG.get("active_profile") or "").strip()
        if ap and ap in profs:
            _ACTIVE_PROFILE = ap
    # Fallback to base config (no profile) if nothing matched
    base = dict(CONFIG)
    # Remove non-capture keys from base
    for rm in ("profiles","active_profile","auto_switch","auto_map"):
        base.pop(rm, None)
    # Merge selected profile on top of base
    if _ACTIVE_PROFILE and _ACTIVE_PROFILE in profs:
        prof = dict(profs[_ACTIVE_PROFILE])
        base.update(prof)
    return base

def _find_window_rect_by_exe_or_title(win_exe: str, win_title: str):
    try:
        import win32gui, win32process  # type: ignore
    except Exception as e:
        raise RuntimeError("pywin32 required for window mode (pip install pywin32)") from e
    target_exe = (win_exe or "").lower().strip()
    target_title = (win_title or "").lower().strip()
    result = None
    def enum_handler(hwnd, ctx):
        nonlocal result
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            title = (win32gui.GetWindowText(hwnd) or "").lower()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            ok = False
            if target_exe:
                try:
                    import psutil  # type: ignore
                    p = psutil.Process(pid)
                    exe = os.path.basename(p.exe() or "") or (p.name() or "")
                    ok = (exe.lower() == target_exe)
                except Exception:
                    ok = False
            if not ok and target_title:
                ok = (target_title in title)
            if ok:
                rect = win32gui.GetWindowRect(hwnd)  # (l,t,r,b)
                # prefer the first match; could refine by size or z-order
                result = rect
        except Exception:
            pass
    try:
        win32gui.EnumWindows(enum_handler, None)
    except Exception:
        pass
    if not result:
        raise RuntimeError("window not found (exe/title)")
    return result

def _grab_dxcam(profile: Dict[str, Any]):
    try:
        import dxcam  # type: ignore
    except Exception as e:
        raise RuntimeError("missing dxcam (pip install dxcam)") from e
    cam = dxcam.create(output_idx=int(profile.get("monitor",0)))
    mode = str(profile.get("mode","region")).lower()
    region = None
    if mode == "region":
        r = profile.get("region") or {}
        l, t = int(r.get("left",0)), int(r.get("top",0))
        w, h = int(r.get("width",800)), int(r.get("height",450))
        region = (l, t, l+w, t+h)
    elif mode == "window":
        rect = _find_window_rect_by_exe_or_title(profile.get("window_exe",""), profile.get("window_title",""))
        region = rect  # (l,t,r,b)
    # else fullscreen -> region=None
    frame = cam.grab(region=region)
    if frame is None:
        raise RuntimeError("dxcam.grab returned None")
    try:
        from PIL import Image  # type: ignore
    except Exception as e:
        raise RuntimeError("missing Pillow (pip install Pillow)") from e
    img = Image.fromarray(frame[..., ::-1])  # BGR->RGB
    path = _png_path("wgc", out_dir=profile.get("out_dir"))
    img.save(path, format="PNG")
    return path

def _grab_mss(profile: Dict[str, Any]):
    try:
        import mss, mss.tools  # type: ignore
    except Exception as e:
        raise RuntimeError("missing mss (pip install mss)") from e
    mode = str(profile.get("mode","region")).lower()
    region = None
    if mode == "region":
        r = profile.get("region") or {}
        l, t = int(r.get("left",0)), int(r.get("top",0))
        w, h = int(r.get("width",800)), int(r.get("height",450))
        region = {"left": l, "top": t, "width": w, "height": h}
    elif mode == "window":
        l, t, r, b = _find_window_rect_by_exe_or_title(profile.get("window_exe",""), profile.get("window_title",""))
        region = {"left": int(l), "top": int(t), "width": int(r-l), "height": int(b-t)}
    with mss.mss() as sct:
        if region is None:
            mon_id = int(profile.get("monitor",0)) + 1
            mon = sct.monitors[mon_id] if mon_id < len(sct.monitors) else sct.monitors[1]
            shot = sct.grab(mon)
        else:
            shot = sct.grab(region)
        path = _png_path("wgc", out_dir=profile.get("out_dir"))
        mss.tools.to_png(shot.rgb, shot.size, output=path)
        return path

def _capture_once(profile: Dict[str, Any]):
    backend = str(profile.get("backend", CONFIG.get("backend","dxcam"))).lower()
    if backend == "dxcam":
        return _grab_dxcam(profile)
    elif backend == "mss":
        return _grab_mss(profile)
    else:
        raise RuntimeError(f"unknown backend: {backend}")

def _consume_profile_switch():
    """Switch profile when a .profile file is dropped; content (first line) = profile name"""
    qd = _queue_dir("wgc_capture")
    files = [x for x in os.listdir(qd) if x.endswith(".profile")]
    for name in files:
        path = os.path.join(qd, name)
        try:
            want = (open(path, "r", encoding="utf-8").read().strip().splitlines() or [""])[0]
            if want and want in (CONFIG.get("profiles") or {}):
                global _ACTIVE_PROFILE
                _ACTIVE_PROFILE = want
            os.rename(path, path + ".done")
        except Exception as ex:
            with open(path + ".err.txt", "w", encoding="utf-8") as f:
                f.write(str(ex) + "\n" + traceback.format_exc())

def _worker():
    while not _STOP.is_set():
        profile = _resolve_profile()
        fps = max(1, int(profile.get("fps", CONFIG.get("fps",20))))
        delay = 1.0 / float(fps)
        try:
            _capture_once(profile)
        except Exception as e:
            qd = _queue_dir("wgc_capture")
            with open(os.path.join(qd, "_last_error.txt"), "w", encoding="utf-8") as f:
                f.write(str(e) + "\n" + traceback.format_exc())
        # one-shot .tick
        try:
            qd = _queue_dir("wgc_capture")
            ticks = [x for x in os.listdir(qd) if x.endswith(".tick")]
            for name in ticks:
                path = os.path.join(qd, name)
                try:
                    _capture_once(profile)
                    os.rename(path, path + ".done")
                except Exception as ex:
                    with open(path + ".err.txt", "w", encoding="utf-8") as f:
                        f.write(str(ex) + "\n" + traceback.format_exc())
        except Exception:
            pass
        # check profile switch files
        _consume_profile_switch()
        _STOP.wait(delay)

def configure(cfg: Dict[str, Any]):
    CONFIG.update(cfg or {})
    return {"ok": True, "applied": CONFIG}

def enable():
    global _ENABLED, _THREAD
    _ENABLED = True
    _ensure_dirs()
    if CONFIG.get("autostart") and _THREAD is None:
        _STOP.clear()
        _THREAD = threading.Thread(target=_worker, daemon=True)
        _THREAD.start()
    return {"ok": True, "enabled": True}

def health():
    profile = _resolve_profile()
    backend = str(profile.get("backend", CONFIG.get("backend","dxcam"))).lower()
    needed = []
    ok = True
    if backend == "dxcam":
        try:
            import dxcam  # type: ignore
        except Exception:
            ok = False; needed.append("pip install dxcam")
    elif backend == "mss":
        try:
            import mss  # type: ignore
        except Exception:
            ok = False; needed.append("pip install mss")
    try:
        from PIL import Image  # type: ignore
    except Exception:
        ok = False; needed.append("pip install Pillow")
    if profile.get("mode","").lower() == "window":
        try:
            import win32gui  # type: ignore
            import psutil     # type: ignore
        except Exception:
            ok = False; needed.append("pip install pywin32 psutil")
    return {"ok": ok, "module": "wgc_capture", "backend": backend, "active_profile": _ACTIVE_PROFILE, "hint": (", ".join(needed) if needed else None)}

try:
    from module_api import register_simple_module  # type: ignore
    register_simple_module("wgc_capture", configure, enable, health)
except Exception:
    pass
