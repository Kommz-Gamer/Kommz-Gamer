# server_info.py — base minimale pour endpoint /api/mod/server_info/health
from flask import Blueprint, jsonify
bp = Blueprint('server_info', __name__)

@bp.route('/api/mod/server_info/health')
def health():
    return jsonify(ok=True, module='server_info', origin='base')
