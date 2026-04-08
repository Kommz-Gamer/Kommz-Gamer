from module_api import register_simple_module
def register(app, cfg=None):
    return register_simple_module(app, "util_sync")
