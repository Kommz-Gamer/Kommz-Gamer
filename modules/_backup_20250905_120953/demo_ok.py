from flask import Blueprint, jsonify

BLUEPRINT = Blueprint("demo_ok", __name__)

@BLUEPRINT.route("/health", methods=["GET"])
def health():
    return jsonify(ok=True, module="demo_ok")

@BLUEPRINT.route("/ping", methods=["GET"])
def ping():
    return jsonify(pong=True, module="demo_ok")

def register(app, base_url="/api/mods/demo_ok"):
    app.register_blueprint(BLUEPRINT, url_prefix=base_url)
