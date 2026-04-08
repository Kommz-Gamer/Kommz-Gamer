# debug_routes.py — base minimale pour endpoint /api/mod/debug_routes/health
from flask import Blueprint, jsonify
bp = Blueprint('debug_routes', __name__)

@bp.route('/api/mod/debug_routes/health')
def health():
    return jsonify(ok=True, module='debug_routes', origin='base')
