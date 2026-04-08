import os
from flask import request, jsonify
from module_api import BaseModule, get_logger

log = get_logger("stt_whisper")

def register(app, cfg=None):
    m = BaseModule("stt_whisper")
    bp = m.blueprint()

    @bp.route("/api/mod/stt_whisper/transcribe", methods=["POST"])
    def transcribe():
        data = request.get_json(silent=True) or {}
        wav = data.get("file")
        model_size = (data.get("model") or (cfg or {}).get("stt_whisper", {}).get("model") or "base")
        if not wav or not os.path.exists(wav):
            return jsonify({"ok": False, "error": "file not found"}), 400
        try:
            from faster_whisper import WhisperModel
        except Exception:
            return jsonify({"ok": False, "error": "faster-whisper not installed"}), 500
        try:
            model = WhisperModel(model_size, device="cpu", compute_type="int8")
            segments, info = model.transcribe(wav, beam_size=1)
            text = "".join(seg.text for seg in segments)
            return jsonify({"ok": True, "text": text, "language": info.language, "prob": info.language_probability})
        except Exception as e:
            log.exception("whisper failed")
            return jsonify({"ok": False, "error": str(e)}), 500

    app.register_blueprint(bp)
    return m
