# Shim 'hello' -> redirige vers modules/hello/hello.py
try:
    from modules.hello.hello import health, configure
except Exception as e:
    def health():
        return {"ok": False, "module": "hello", "error": f"shim import failed: {e}"}
    def configure(**kwargs):
        return {"ok": False, "module": "hello", "error": f"shim import failed: {e}"}
