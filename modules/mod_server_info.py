# mod_server_info.py
from flask import Blueprint, jsonify
import os, platform, time

bp = Blueprint("mod_server_info", __name__, url_prefix="/api/mod/server_info")

@bp.route("/health")
def health():
    return jsonify(ok=True, module="server_info")

@bp.route("/info")
def info():
    return jsonify(
        ok=True,
        time=time.strftime("%Y-%m-%d %H:%M:%S"),
        os=platform.platform(),
        py=platform.python_version(),
        cwd=os.getcwd()
    )

def register(app):
    app.register_blueprint(bp)
    return bp
