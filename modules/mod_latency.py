# mod_latency.py — Endpoint utilitaire /ping (standalone)
from flask import Blueprint, jsonify, request
import os, subprocess, re, time, socket

bp2 = Blueprint("latency_util_bp", __name__)

def _win_ping_candidates():
    windir = os.environ.get("WINDIR", r"C:\Windows")
    return [
        os.path.join(windir, "System32", "ping.exe"),
        os.path.join(windir, "Sysnative", "ping.exe"),
        "ping",
    ]

def _parse_ping_ms(text: str):
    pats = [
        r"(?:Temps|Durée|Duree|time)\s*[=<]\s*(\d+)\s*ms",
        r"(?:Average|Moyenne)\s*=\s*(\d+)\s*ms",
        r"Minimum\s*=\s*(\d+)\s*ms.*Maximum\s*=\s*(\d+)\s*ms.*(?:Average|Moyenne)\s*=\s*(\d+)\s*ms",
    ]
    import re
    for p in pats:
        m = re.search(p, text, re.IGNORECASE | re.DOTALL)
        if m:
            if len(m.groups()) == 3:
                return int(m.group(3))
            return int(m.group(1))
    if re.search(r"<\s*1\s*ms|<1ms", text, re.IGNORECASE):
        return 1
    return None

def _icmp_ping(host: str, count=1, timeout_ms=1200):
    for exe in _win_ping_candidates():
        try:
            out = subprocess.check_output([exe, "-n", str(count), "-w", str(timeout_ms), host],
                                          stderr=subprocess.STDOUT, text=True, encoding="utf-8", shell=False)
            ms = _parse_ping_ms(out)
            if ms is not None:
                return ms, "icmp"
        except Exception:
            pass
    try:
        out = subprocess.check_output(f'cmd /c ping -n {count} -w {timeout_ms} {host}',
                                      stderr=subprocess.STDOUT, text=True, encoding="utf-8", shell=True)
        ms = _parse_ping_ms(out)
        if ms is not None:
            return ms, "icmp"
    except Exception:
        pass
    return None, None

def _tcp_latency(host: str, port=443, timeout=1.5):
    try:
        t0 = time.perf_counter()
        with socket.create_connection((host, port), timeout=timeout):
            pass
        dt = (time.perf_counter() - t0) * 1000.0
        return int(round(dt)), f"tcp:{port}"
    except Exception:
        return None, None

@bp2.route("/ping")
def ping():
    host = (request.args.get("host") or "1.1.1.1").strip()
    port = int(request.args.get("port") or 443)
    ms, via = _icmp_ping(host)
    if ms is None:
        ms, via = _tcp_latency(host, port)
    return jsonify(ok=(ms is not None), ms=ms, via=via, host=host, port=port)

def register(app):
    app.register_blueprint(bp2, url_prefix="/api/mod/latency")
