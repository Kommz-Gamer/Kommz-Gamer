# VTP stats module (no external deps)
from flask import Blueprint, jsonify, current_app, request
import time, urllib.request, urllib.error, json

stats_bp = Blueprint("stats", __name__, url_prefix="/api/track")

def iter_health_endpoints():
    eps = []
    for rule in current_app.url_map.iter_rules():
        r = str(rule.rule)
        if r.startswith("/api/mod/") and (r.endswith("/health") or r.endswith("/wrap/health")):
            eps.append(r)
    eps.sort()
    return eps

@stats_bp.route("/debug/health_endpoints")
def debug_health_endpoints():
    eps = iter_health_endpoints()
    return jsonify(count=len(eps), endpoints=eps)

@stats_bp.route("/stats2")
def stats2():
    eps = iter_health_endpoints()
    base = request.host_url.rstrip("/")  # http://127.0.0.1:8770
    details = []
    ok = err = 0
    for ep in eps:
        url = f"{base}{ep}"
        t0 = time.perf_counter()
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"VTP-Stats"})
            with urllib.request.urlopen(req, timeout=2.5) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
            ms = int((time.perf_counter() - t0) * 1000)
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {"raw": raw[:200]}
            details.append({"endpoint": ep, "ok": True, "ms": ms, "data": payload})
            ok += 1
        except Exception as e:
            ms = int((time.perf_counter() - t0) * 1000)
            details.append({"endpoint": ep, "ok": False, "ms": ms, "error": str(e)})
            err += 1
    return jsonify(counts={"total": len(eps), "ok": ok, "err": err},
                   scan_ms=sum(d["ms"] for d in details),
                   details=details)

@stats_bp.route("/stats")
def stats():
    # legacy shape
    base = request.host_url.rstrip("/")
    ok_eps = []
    for ep in iter_health_endpoints():
        try:
            with urllib.request.urlopen(f"{base}{ep}", timeout=2.5) as _:
                ok_eps.append(ep)
        except Exception:
            pass
    return jsonify(ok=True, stats={"health_ok": ok_eps})

def register(app):
    app.register_blueprint(stats_bp)
    return stats_bp
