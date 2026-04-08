# -*- coding: utf-8 -*-
"""
Valorant Translator Pro - Launcher (patched)
- Sert le dashboard via /ui/ (API sur 8770) + serveurs statiques optionnels 8765/8790
- API: /api/health, /api/ping, /api/track/stats (+ /api/debug/*)
- Scan récursif du dossier modules (ignore __init__.py, module_api.py, fichiers _*)
- Supporte BLUEPRINT et/ou register(app, base_url)
- Shim module_api (BaseModule, get_logger, etc.)
- Evite collisions de Blueprint (skip avec log)
"""

import sys, os, json, time, threading, types
from pathlib import Path
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from flask import Flask, jsonify, Blueprint, current_app, send_from_directory, redirect

# ----------------------------
# App root (PyInstaller friendly)
# ----------------------------
if getattr(sys, "frozen", False):
    APP_ROOT = Path(sys.executable).resolve().parent
else:
    APP_ROOT = Path(__file__).resolve().parent

CONFIG_DIR   = APP_ROOT / "config"
CONFIG_FILE  = CONFIG_DIR / "config.json"
CONFIG_DEF   = CONFIG_DIR / "config.default.json"
DASH_DIR     = APP_ROOT / "dashboard"
OVERLAY_DIR  = APP_ROOT / "overlay"
MODULES_DIR  = APP_ROOT / "modules"

# ----------------------------
# Logging minimal
# ----------------------------
def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg: str):
    line = f"[{ts()}] {msg}"
    print(line, flush=True)
    try:
        (APP_ROOT / "logs").mkdir(exist_ok=True)
        with (APP_ROOT / "logs" / "launcher.log").open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

# ----------------------------
# Config par défaut
# ----------------------------
DEFAULT_CONFIG = {
    "api": {"host": "127.0.0.1", "port": 8770},
    "ui": {
        "dashboard_host": "127.0.0.1",
        "dashboard_port": 8765,
        "overlay_host":   "127.0.0.1",
        "overlay_port":   8790,
        "writePlaceholder": False,  # ne pas créer de placeholder UI
        "allowCORS": True
    }
}

def safe_read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"[WARN] Failed to read {p.name}, using default. {e}")
        return None

def write_default_configs_if_missing():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_DEF.exists():
        CONFIG_DEF.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
        log("Wrote default config.default.json")
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(CONFIG_DEF.read_text(encoding="utf-8"), encoding="utf-8")
        log("Created config.json from default")

# ----------------------------
# UI: ne pas écraser index.html/overlay.html
# ----------------------------
def ensure_ui_files(allow_placeholder: bool):
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)

    dash_index = DASH_DIR / "index.html"
    ovl_html   = OVERLAY_DIR / "overlay.html"

    if not dash_index.exists():
        if allow_placeholder:
            dash_index.write_text(
                "<!doctype html><title>Dashboard</title>"
                "<body style='color:#ddd;background:#111;font:14px system-ui'>Dashboard prêt.</body>",
                encoding="utf-8"
            )
            log("Wrote dashboard/index.html (placeholder)")
        else:
            log("[UI] dashboard/index.html manquant (placeholder désactivé).")

    if not ovl_html.exists():
        if allow_placeholder:
            ovl_html.write_text(
                "<!doctype html><title>Overlay</title>"
                "<body style='color:#ddd;background:#111;font:14px system-ui'>Overlay prêt.</body>",
                encoding="utf-8"
            )
            log("Wrote overlay/overlay.html (placeholder)")
        else:
            log("[UI] overlay/overlay.html manquant (placeholder désactivé).")

# ----------------------------
# Serveur statique sans changer le CWD (optionnel)
# ----------------------------
class ReusableTCPServer(TCPServer):
    allow_reuse_address = True

def make_handler(root_dir: Path):
    class QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(root_dir), **kwargs)
        def log_message(self, format, *args):
            pass
    return QuietHandler

def start_static_server(root_dir: Path, host: str, port: int, label: str):
    def _run():
        try:
            Handler = make_handler(root_dir)
            with ReusableTCPServer((host, port), Handler) as httpd:
                log(f"Serving '{root_dir}' at http://{host}:{port}/")
                httpd.serve_forever()
        except OSError as e:
            log(f"[ERR] Static server {root_dir} on {host}:{port} failed: {e}")
        except Exception as e:
            log(f"[ERR] Static server {label} crashed: {e}")
    t = threading.Thread(target=_run, name=f"Static-{label}", daemon=True)
    t.start()
    return t

# ----------------------------
# Shim module_api (pour compat legacy)
# ----------------------------
def install_module_api_shim():
    if "module_api" in sys.modules:
        return
    mod = types.ModuleType("module_api")

    # Expose éléments Flask utiles
    mod.Blueprint   = Blueprint
    mod.jsonify     = jsonify
    mod.current_app = current_app

    # Décorateur light
    def route(bp, rule, methods=None):
        methods = methods or ["GET"]
        def deco(fn):
            bp.route(rule, methods=methods)(fn)
            return fn
        return deco

    # Fabrique de Blueprint avec url_prefix facultatif
    def make_blueprint(name, url_prefix=None):
        bp = Blueprint(f"mod_{name}", __name__)
        bp._mod_url_prefix = url_prefix or f"/api/mods/{name}"
        return bp

    # Logger simple compatible
    class ModuleLogger:
        def __init__(self, name): self.name = name
        def info(self, m):  log(f"[MOD/{self.name}] {m}")
        def warn(self, m):  log(f"[MOD/{self.name}][WARN] {m}")
        def error(self, m): log(f"[MOD/{self.name}][ERR] {m}")

    def get_logger(name):  # demandé par des modules
        return ModuleLogger(name)

    # BaseModule minimaliste (souvent hérité)
    class BaseModule:
        def __init__(self, name, app=None, base_url=""):
            self.name = name
            self.app = app
            self.base_url = base_url
            self.logger = ModuleLogger(name)
        def register(self, app, base_url=None):
            self.app = app
            if base_url: self.base_url = base_url

    # Contexte utilitaire
    class ModuleContext:
        def __init__(self, name, app=None, base_url=""):
            self.name = name
            self.app = app
            self.base_url = base_url
            self.logger = ModuleLogger(name)

    # Aliases/exports
    mod.route          = route
    mod.make_blueprint = make_blueprint
    mod.ModuleLogger   = ModuleLogger
    mod.get_logger     = get_logger
    mod.logger         = get_logger      # alias
    mod.BaseModule     = BaseModule
    mod.ModuleContext  = ModuleContext

    sys.modules["module_api"] = mod

# ----------------------------
# Chargement de modules (scan récursif)
# ----------------------------
class ModuleInfo:
    def __init__(self, name, file, ok, error=""):
        self.name  = name
        self.file  = str(file)
        self.ok    = ok
        self.error = error

def load_modules(flask_app: Flask, base_api="/api/mods"):
    """
    Charge tous les .py dans MODULES_DIR (récursif).
    - Ignore __init__.py, module_api.py, fichiers commençant par _ ou .
    - Enregistre BLUEPRINT ou register(app, base_url); sinon 'chargé sans endpoint'.
    """
    MODULES_DIR.mkdir(exist_ok=True)

    log(f"[MOD] Scanning dir: {MODULES_DIR}")
    if not MODULES_DIR.exists():
        log("[MOD] Modules dir does not exist.")
        return []

    files = [p for p in MODULES_DIR.rglob("*.py")
             if p.name not in ("__init__.py", "module_api.py")
             and not p.name.startswith(("_", "."))]

    log(f"[MOD] Found {len(files)} module file(s).")
    for p in files[:10]:
        try:
            rel = p.relative_to(MODULES_DIR)
            log(f"[MOD] · {rel}")
        except Exception:
            log(f"[MOD] · {p}")
    if len(files) > 10:
        log(f"[MOD] · (+{len(files)-10} more)")

    loaded = []
    import importlib.util
    install_module_api_shim()

    for f in files:
        # Nom logique basé sur le chemin relatif (compatible sous-dossiers)
        rel = f.relative_to(MODULES_DIR).with_suffix('')
        name = rel.as_posix().replace('/', '_')  # ex: tts/edge.py -> tts_edge
        try:
            spec = importlib.util.spec_from_file_location(f"vtp_mod_{name}", f)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)  # type: ignore

            # 1) Blueprint explicite (gérer collision)
            bp = getattr(mod, "BLUEPRINT", None)
            if isinstance(bp, Blueprint):
                bp_name = getattr(bp, "name", f"mod_{name}")
                if bp_name in flask_app.blueprints:
                    log(f"[MOD][WARN] Blueprint collision '{bp_name}', skipping file {f.name}")
                    loaded.append(ModuleInfo(name, f, False, f"blueprint '{bp_name}' already registered"))
                    continue

                url_prefix = getattr(bp, "_mod_url_prefix", f"{base_api}/{name}")
                flask_app.register_blueprint(bp, url_prefix=url_prefix)
                log(f"[MOD] Chargé (bp): {f.name} -> {url_prefix}")
                loaded.append(ModuleInfo(name, f, True))
                continue

            # 2) Fonction register(...)
            reg = getattr(mod, "register", None)
            if callable(reg):
                url_prefix = f"{base_api}/{name}"
                try:
                    reg(flask_app, url_prefix)
                except TypeError:
                    reg(flask_app)  # fallback si signature différente
                log(f"[MOD] Chargé (register): {f.name} -> {url_prefix}")
                loaded.append(ModuleInfo(name, f, True))
                continue

            # 3) Import OK mais pas d'endpoint
            log(f"[MOD] Chargé (sans endpoint): {f.name}")
            loaded.append(ModuleInfo(name, f, True))

        except Exception as e:
            log(f"[MOD] ERREUR {f.name}: {e}")
            loaded.append(ModuleInfo(name, f, False, str(e)))

    return loaded

# ----------------------------
# Attacher les routes API + UI + Debug
# ----------------------------
def attach_api_routes(app: Flask, cfg, loaded_modules_initial):
    ui_cfg = (cfg or {}).get("ui", {})
    if ui_cfg.get("allowCORS", True):
        dash_host = ui_cfg.get("dashboard_host", "127.0.0.1")
        dash_port = ui_cfg.get("dashboard_port", 8765)
        allowed = f"http://{dash_host}:{dash_port}"

        @app.after_request
        def _cors(resp):
            resp.headers["Access-Control-Allow-Origin"] = allowed
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
            resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
            return resp

        log("[API] CORS enabled for dashboard")

    # ---- API core ----
    @app.route("/api/health")
    def api_health():
        return jsonify(ok=True, time=ts())

    @app.route("/api/ping")
    def api_ping():
        return jsonify(pong=True, time=ts())

    @app.route("/api/track/stats")
    def api_stats():
        mods_runtime = current_app.config.get("LOADED_MODULES", loaded_modules_initial) or []
        mods = [{
            "name": m.name,
            "file": m.file,
            "ok":   m.ok,
            "error":m.error
        } for m in mods_runtime]
        totals = {
            "total": len(mods),
            "ok":    sum(1 for m in mods if m["ok"]),
            "err":   sum(1 for m in mods if not m["ok"]),
        }
        return jsonify(ok=True, modules=mods, counts=totals, time=ts())

    # ---- UI via 8770 (sert ton dashboard) ----
    @app.route("/")
    def root_redirect_to_ui():
        return redirect("/ui/", code=302)

    @app.route("/ui/")
    def ui_index():
        index = DASH_DIR / "index.html"
        if index.exists():
            return send_from_directory(str(DASH_DIR), "index.html")
        return jsonify(ok=False, error="dashboard/index.html introuvable", hint=str(index)), 404

    @app.route("/ui/<path:filename>")
    def ui_files(filename):
        return send_from_directory(str(DASH_DIR), filename)

    # ---- Debug: modules ----
    @app.route("/api/debug/modules_dir")
    def dbg_modules_dir():
        return jsonify(path=str(MODULES_DIR), exists=MODULES_DIR.exists())

    @app.route("/api/debug/modules_files")
    def dbg_modules_files():
        files = []
        if MODULES_DIR.exists():
            for p in MODULES_DIR.rglob("*.py"):
                if p.name in ("__init__.py", "module_api.py") or p.name.startswith(("_",".")):
                    continue
                try:
                    files.append(str(p.relative_to(MODULES_DIR)))
                except Exception:
                    files.append(str(p))
        return jsonify(count=len(files), files=files)

# ----------------------------
# Main
# ----------------------------
def ensure_ports(ui_cfg):
    # Optionnel: démarrer serveurs statiques pour compat overlay/dashboard
    try:
        host_dash = ui_cfg.get("dashboard_host", "127.0.0.1")
        port_dash = int(ui_cfg.get("dashboard_port", 8765))
        start_static_server(DASH_DIR, host_dash, port_dash, "dashboard")
    except Exception as e:
        log(f"[ERR] Dashboard server failed: {e}")

    try:
        host_ovl = ui_cfg.get("overlay_host", "127.0.0.1")
        port_ovl = int(ui_cfg.get("overlay_port", 8790))
        start_static_server(OVERLAY_DIR, host_ovl, port_ovl, "overlay")
    except Exception as e:
        log(f"[ERR] Overlay server failed: {e}")

def main():
    log("=== Valorant Translator Pro starting ===")
    log(f"App root: {APP_ROOT}")

    # 1) Configs
    write_default_configs_if_missing()
    cfg = safe_read_json(CONFIG_FILE)
    if cfg is None:
        cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    log(f"Config: {CONFIG_FILE}")

    # ----- Override du dossier modules via config/env -----
    ext_mod = os.getenv("VTP_MODULES_DIR") or ((cfg or {}).get("modules", {}) or {}).get("path")
    if ext_mod:
        p = Path(ext_mod)
        if p.exists():
            global MODULES_DIR
            MODULES_DIR = p
            log(f"[MOD] Using external modules dir: {MODULES_DIR}")
        else:
            log(f"[MOD][WARN] External modules dir not found: {p} -> fallback to {MODULES_DIR}")
    # ------------------------------------------------------

    # 2) UI (placeholders désactivés par défaut, sauf si autorisés)
    ui_cfg = (cfg or {}).get("ui", {})
    env_no_ph = os.getenv("VTP_NO_PLACEHOLDER_UI", "0") == "1"
    allow_placeholder = bool(ui_cfg.get("writePlaceholder", False)) and (not env_no_ph)
    ensure_ui_files(allow_placeholder=allow_placeholder)

    # 3) Serveurs statiques optionnels
    ensure_ports(ui_cfg)

    # 4) API + Modules (même app)
    api_cfg = (cfg or {}).get("api", {})
    api_host = api_cfg.get("host", "127.0.0.1")
    api_port = int(api_cfg.get("port", 8770))

    app = Flask("VTP_API")
    mods = load_modules(app, base_api="/api/mods")
    app.config["LOADED_MODULES"] = mods
    attach_api_routes(app, cfg, mods)

    log(f"API served at http://{api_host}:{api_port}/ (requested {api_port})")

    def run_api():
        try:
            app.run(host=api_host, port=api_port, debug=False, threaded=True, use_reloader=False)
        except OSError as e:
            log(f"[ERR] API failed to bind on {api_host}:{api_port} - {e}")

    t_api = threading.Thread(target=run_api, name="FlaskAPI", daemon=True)
    t_api.start()

    # 5) Boucle keep-alive
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
