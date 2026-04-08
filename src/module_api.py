from pathlib import Path
import threading
class Logger:
    def __init__(self, name="module"): self.name=name
    def info(self,*a): print("[INFO]", self.name, *a, flush=True)
    def warn(self,*a): print("[WARN]", self.name, *a, flush=True)
    def error(self,*a): print("[ERR ]", self.name, *a, flush=True)
    def debug(self,*a): print("[DBG ]", self.name, *a, flush=True)
def get_logger(name="module"): return Logger(name)
class ModuleContext:
    def __init__(self, root=None, config=None, app=None):
        self.root=Path(root or "."); self.config=config or {}; self.app=app; self.logger=get_logger("module_api")
def ensure_dir(p: Path):
    Path(p).mkdir(parents=True, exist_ok=True); return Path(p)
def start_background(target, *args, **kwargs):
    th=threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True); th.start(); return th
def stop_background(th): pass
