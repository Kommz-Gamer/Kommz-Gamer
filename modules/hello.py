# auto-shim -> redirige vers modules/hello/hello.py si présent
try:
    from modules.hello.hello import health, configure
except Exception as e:
    def health():
        return {"ok": True, "module": "hello", "note": "shim active (base non trouvé)", "err": str(e)}
    def configure(**kwargs):
        return {"ok": True, "module": "hello", "updated": list(kwargs.keys()), "note": "shim"}
