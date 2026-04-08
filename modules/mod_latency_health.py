# mod_latency_health.py — Health endpoint pour latence (standalone)
from flask import Blueprint, jsonify, request
import os, subprocess, re, time, socket

bp = Blueprint("latency_health_bp", __name__)

HOST_CANDIDATES = [
    "1.1.1.1",            # Cloudflare
    "8.8.8.8",            # Google DNS
    "9.9.9.9",            # Quad9
    "cloudflare-dns.com",
    "google.com",
    "one.one.one.one",
]
TCP_PORTS = [443, 80]

def _win_ping_candidates():
    windir = os.environ.get("WINDIR", r"C:\Windows")
    return [
        os.path.join(windir, "System32", "ping.exe"),
        os.path.join(windir, "Sysnative", "ping.exe"),
        "ping",  # fallback PATH
    ]

def _parse_ping_ms(text: str):
    # time=12ms | Temps=12 ms | Durée = 10 ms | Average = 12ms | <1ms
    pats = [
        r"(?:Temps|Durée|Duree|time)\s*[=<]\s*(\d+)\s*ms",
        r"(?:Average|Moyenne)\s*=\s*(\d+)\s*ms",
        r"Minimum\s*=\s*(\d+)\s*ms.*Maximum\s*=\s*(\d+)\s*ms.*(?:Average|Moyenne)\s*=\s*(\d+)\s*ms",
    ]
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
    # fallback via cmd
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

def _try_host(host: str):
    ms, via = _icmp_ping(host)
    if ms is not None:
        return ms, via
    for p in TCP_PORTS:
        ms, via = _tcp_latency(host, p)
        if ms is not None:
            return ms, via
    return None, None

@bp.route("/health")
def health():
    # On priorise le host= passé en query, sinon on teste une liste jusqu’à succès.
    first = (request.args.get("host") or "").strip()
    tried = []
    if first:
        ms, via = _try_host(first)
        if ms is not None:
            return jsonify(ok=True, module="latency", ms=ms, via=via, host=first)
        tried.append(first)
    for h in HOST_CANDIDATES:
        ms, via = _try_host(h)
        if ms is not None:
            return jsonify(ok=True, module="latency", ms=ms, via=via, host=h)
        tried.append(h)
    return jsonify(ok=False, module="latency", ms=None, via=None, host=(first or None), tried=tried)

def register(app):
    app.register_blueprint(bp, url_prefix="/api/mod/latency")
