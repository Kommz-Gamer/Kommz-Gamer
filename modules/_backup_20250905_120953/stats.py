from flask import Blueprint, jsonify, current_app

bp = Blueprint("stats", __name__)

@bp.route("/api/track/health", methods=["GET"])
def track_health():
    return jsonify({"ok": True})

@bp.route("/api/track/endpoints", methods=["GET"])
def track_endpoints():
    eps = []
    for rule in current_app.url_map.iter_rules():
        u = str(rule)
        if u.startswith("/api/mod/") and u.endswith("/health"):
            eps.append(u)
    return jsonify({"count": len(eps), "endpoints": sorted(eps)})

@bp.route("/api/track/stats", methods=["GET"])
def track_stats():
    with current_app.test_client() as c:
        eps = track_endpoints().json.get("endpoints", [])
        ok = 0
        for e in eps:
            r = c.get(e)
            j = r.json if r.is_json else {}
            if r.status_code == 200 and j.get("ok") is True:
                ok += 1
    return jsonify({"ok": True, "stats": {"total": len(eps), "ok": ok, "err": len(eps)-ok}})

@bp.route("/api/track/stats2", methods=["GET"])
def track_stats2():
    details = []
    with current_app.test_client() as c:
        eps = track_endpoints().json.get("endpoints", [])
        for e in eps:
            r = c.get(e)
            j = r.json if r.is_json else {}
            details.append({"endpoint": e, "ok": (r.status_code==200 and j.get("ok") is True), "data": j, "ms": 0})
    counts = {"total": len(details), "ok": sum(d["ok"] for d in details), "err": sum(1 for d in details if not d["ok"])}
    return jsonify({"counts": counts, "details": details, "scan_ms": 0})
