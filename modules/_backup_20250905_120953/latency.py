# latency.py — base minimale pour endpoint /api/mod/latency/health
from flask import Blueprint, jsonify
bp = Blueprint('latency', __name__)

@bp.route('/api/mod/latency/health')
def health():
    return jsonify(ok=True, module='latency', origin='base')
