import subprocess, os, sys, tempfile
from datetime import datetime
from flask import request, jsonify, current_app
from module_api import BaseModule

def register(app, cfg=None):
    m = BaseModule("tts_pwsh")
    bp = m.blueprint()

    @bp.route("/api/mod/tts_pwsh/say", methods=["POST"])
    def say():
        data = request.get_json(silent=True) or {}
        text = data.get("text") or ""
        if not text.strip():
            return jsonify({"ok": False, "error": "text is empty"}), 400
        out_dir = os.path.join(current_app.root_path, "output", "tts_pwsh")
        os.makedirs(out_dir, exist_ok=True)
        out_wav = os.path.join(out_dir, f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
        # PowerShell one-liner to SAPI TTS -> WAV
        ps = f"$t='{text.replace('"','`"')}';$sp=New-Object -ComObject SAPI.SpVoice;" \                 f"$fs=New-Object -ComObject SAPI.SpFileStream;$fs.Open('{out_wav}',3);$sp.AudioOutputStream=$fs;" \                 f"$sp.Speak($t);$fs.Close();"
        try:
            subprocess.run(["powershell","-NoLogo","-NoProfile","-Command", ps], check=True, capture_output=True, text=True)
            return jsonify({"ok": True, "file": out_wav})
        except subprocess.CalledProcessError as e:
            return jsonify({"ok": False, "error": e.stderr or str(e)})

    app.register_blueprint(bp)
    return m
