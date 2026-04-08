# module_api.py — API minimale commune
from dataclasses import dataclass
from flask import Blueprint

@dataclass
class ModuleInfo:
    name: str
    version: str = "1.0"
    author: str = "VTP"

class BaseModule:
    def __init__(self, name: str):
        self.name = name
        self.bp = Blueprint(name, __name__)

def get_logger():
    import logging, sys
    logger = logging.getLogger("VTP.modules")
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter('[%(asctime)s] [MOD] %(message)s'))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger
