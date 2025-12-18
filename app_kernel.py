# app_kernel.py
from ai_core import ai_log, ai_exception

class AppKernel:
    def __init__(self):
        ai_log("kernel", "AppKernel initialized")

    def on_start(self):
        ai_log("kernel", "App started")

    def on_button(self, name):
        ai_log("ui", f"Button pressed: {name}")
        return f"{name} OK"