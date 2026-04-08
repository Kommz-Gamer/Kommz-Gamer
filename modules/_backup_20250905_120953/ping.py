from flask import jsonify
from module_api import BaseModule

def register(app, cfg=None):
    m = BaseModule("ping")
    bp = m.blueprint()

    @bp.route("/api/mod/ping/ping", methods=["GET"])
    def do_ping():
        return jsonify({"ok": True, "pong": True})

    app.register_blueprint(bp)
    return m
