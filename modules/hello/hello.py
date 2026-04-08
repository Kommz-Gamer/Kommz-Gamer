def health():
    return {"ok": True, "module": "hello", "note": "base OK"}

def configure(**kwargs):
    out = {"ok": True, "module": "hello"}
    out.update(kwargs)
    return out
