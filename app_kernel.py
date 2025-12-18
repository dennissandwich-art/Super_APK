# app_kernel.py
from ai_core import ai_log, ai_exception
import time

class AppKernel:
    def __init__(self):
        self.boot_ts = time.time()
        self.state = {
            "booted": False,
            "last_action": None,
            "errors": 0
        }
        ai_log("kernel", "AppKernel constructed")

    # ---------- LIFECYCLE ----------

    def on_start(self):
        try:
            self.state["booted"] = True
            ai_log("kernel", "Kernel start complete")
        except Exception as e:
            self.state["errors"] += 1
            ai_exception("kernel", e)

    def on_resume(self):
        try:
            ai_log("runtime", "App resumed")
        except Exception as e:
            self.state["errors"] += 1
            ai_exception("runtime", e)

    def on_pause(self):
        try:
            ai_log("runtime", "App paused")
        except Exception as e:
            self.state["errors"] += 1
            ai_exception("runtime", e)

    # ---------- UI ENTRY POINTS ----------

    def on_button(self, button_id: str):
        try:
            self.state["last_action"] = button_id
            ai_log("ui", f"Button event: {button_id}")

            if button_id == "get_started":
                return self._handle_get_started()

            if button_id == "settings":
                return self._handle_settings()

            return "UNKNOWN_ACTION"

        except Exception as e:
            self.state["errors"] += 1
            ai_exception("ui", e)
            return "ERROR"

    # ---------- HANDLERS ----------

    def _handle_get_started(self):
        ai_log("kernel", "Get Started executed")
        return "KERNEL_OK"

    def _handle_settings(self):
        ai_log("kernel", "Settings executed")
        return "SETTINGS_OK"

    # ---------- DIAGNOSTICS ----------

    def health_snapshot(self):
        try:
            uptime = int(time.time() - self.boot_ts)
            snapshot = {
                "uptime_sec": uptime,
                "booted": self.state["booted"],
                "last_action": self.state["last_action"],
                "error_count": self.state["errors"]
            }
            ai_log("runtime", f"Health: {snapshot}")
            return snapshot
        except Exception as e:
            ai_exception("runtime", e)
            return None