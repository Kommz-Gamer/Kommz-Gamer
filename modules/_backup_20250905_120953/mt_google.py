import json, urllib.parse, urllib.request
from flask import request, jsonify
from module_api import BaseModule, get_logger

log = get_logger("mt_google")

def _fallback_translate(text, target="en", source="auto"):
    # public endpoint (no key, best-effort)
    params = {
        "client": "gtx",
        "sl": source, "tl": target,
        "dt": "t",
        "q": text
    }
    url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=10) as r:
        data = json.loads(r.read().decode("utf-8"))
    # data[0] is list of [translated, original, ...]
    translated = "".join(seg[0] for seg in data[0] if seg[0])
    return translated

def register(app, cfg=None):
    m = BaseModule("mt_google")
    bp = m.blueprint()

    @bp.route("/api/mod/mt_google/translate", methods=["POST"])
    def translate():
        data = request.get_json(silent=True) or {}
        txt = data.get("text") or ""
        tgt = (data.get("target") or "en").lower()
        src = (data.get("source") or "auto").lower()
        if not txt.strip():
            return jsonify({"ok": False, "error": "text is empty"}), 400
        try:
            out = _fallback_translate(txt, tgt, src)
            return jsonify({"ok": True, "src": src, "tgt": tgt, "text": txt, "translation": out})
        except Exception as e:
            log.exception("translate failed")
            return jsonify({"ok": False, "error": str(e)}), 500

    app.register_blueprint(bp)
    return m
