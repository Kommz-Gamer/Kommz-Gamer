from flask import jsonify
from module_api import BaseModule

def register(app, cfg=None):
    m = BaseModule("recorder")
    bp = m.blueprint()

    @bp.route("/api/mod/recorder/start", methods=["POST"])
    def start():
        return jsonify({"ok": True, "recording": True})

    @bp.route("/api/mod/recorder/stop", methods=["POST"])
    def stop():
        return jsonify({"ok": True, "recording": False})

    app.register_blueprint(bp)
    return m
