# modules/mod_debug_routes.py
from flask import Blueprint, jsonify

def register(app):
    bp = Blueprint("debug_routes_bp", __name__)

    @bp.route("/api/debug/routes", methods=["GET"])
    def routes():
        routes = []
        for r in app.url_map.iter_rules():
            routes.append(str(r))
        routes.sort()
        return jsonify({"count": len(routes), "routes": routes})

    app.register_blueprint(bp)
