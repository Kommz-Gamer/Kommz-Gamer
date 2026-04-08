# Auto-generated wrapper (FIXED) for tts_elevenlabs
# - No dependency on module_api
# - Avoids blueprint collisions by checking existing routes first
# - Registers /api/mod/tts_elevenlabs/health ONLY if missing
# - Always exposes /api/mod/tts_elevenlabs/wrap/health for debugging

import os, importlib.util
from flask import Blueprint, jsonify

MOD_NAME = "tts_elevenlabs"
BP_NAME  = "wrap_" + MOD_NAME
URL_BASE = "/api/mod/" + MOD_NAME

def _try_import_underlying():
    here = os.path.dirname(__file__)
    target = os.path.join(here, f"tts_elevenlabs.py")
    if not os.path.isfile(target):
        return None, "missing base module file"
    try:
        spec = importlib.util.spec_from_file_location("wrapped_" + MOD_NAME, target)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        # optional self-test
        if hasattr(m, "self_test"):
            try:
                m.self_test()
            except Exception as _e:
                return m, f"self_test failed: {_e}"
        return m, None
    except Exception as e:
        return None, str(e)

def register(app):
    # FIX: single-brace set, not nested braces
    existing_routes = {rule.rule for rule in app.url_map.iter_rules()}
    bp = Blueprint(BP_NAME, __name__, url_prefix=URL_BASE)

    want = URL_BASE + "/health"
    if want not in existing_routes:
        @bp.route("/health", methods=["GET"])
        def health():
            mod, err = _try_import_underlying()
            ok = err is None
            return jsonify(ok=ok, module=MOD_NAME, wrapper="health", error=err)

    @bp.route("/wrap/health", methods=["GET"])
    def health_wrap():
        mod, err = _try_import_underlying()
        ok = err is None
        return jsonify(ok=ok, module=MOD_NAME, wrapper="wrap", error=err)

    app.register_blueprint(bp)
    return bp
