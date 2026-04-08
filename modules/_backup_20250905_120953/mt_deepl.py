import os, json
from flask import request, jsonify
from module_api import BaseModule, get_logger

log = get_logger("mt_deepl")

def register(app, cfg=None):
    m = BaseModule("mt_deepl")
    bp = m.blueprint()

    @bp.route("/api/mod/mt_deepl/translate", methods=["POST"])
    def translate():
        data = request.get_json(silent=True) or {}
        txt = data.get("text") or ""
        tgt = (data.get("target") or "EN").upper()
        api_key = (cfg or {}).get("deepl", {}).get("api_key") or os.getenv("DEEPL_API_KEY")
        if not txt.strip():
            return jsonify({"ok": False, "error": "text is empty"}), 400
        if not api_key:
            return jsonify({"ok": False, "error": "DEEPL_API_KEY missing"}), 400
        try:
            import requests
        except Exception:
            return jsonify({"ok": False, "error": "python-requests is required"}), 500
        try:
            r = requests.post("https://api-free.deepl.com/v2/translate",
                              data={"text": txt, "target_lang": tgt},
                              headers={"Authorization": f"DeepL-Auth-Key {api_key}"}, timeout=15)
            j = r.json()
            if "translations" in j:
                return jsonify({"ok": True, "src": j["translations"][0].get("detected_source_language"),
                                "tgt": tgt, "text": txt, "translation": j["translations"][0]["text"]})
            return jsonify({"ok": False, "error": j}), 502
        except Exception as e:
            log.exception("deepl failed")
            return jsonify({"ok": False, "error": str(e)}), 500

    app.register_blueprint(bp)
    return m
