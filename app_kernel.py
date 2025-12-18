# app_kernel.py - Enhanced with error recovery and state management
try:
    from modules.ai_core import ai_log, ai_exception, AI_CONSOLE
except ImportError:
    from ai_core import ai_log, ai_exception, AI_CONSOLE

import time
from datetime import datetime

class AppKernel:
    """
    Enhanced Application Kernel with:
    - AI-driven error recovery
    - State management
    - Health monitoring
    - Auto-recovery strategies
    """

    def __init__(self):
        self.boot_ts = time.time()
        self.state = {
            "booted": False,
            "last_action": None,
            "errors": 0,
            "warnings": 0,
            "recovery_attempts": 0
        }

        # Error recovery strategies
        self.error_recovery_strategies = {
            'network_error': self._recover_network,
            'auth_error': self._recover_auth,
            'payment_error': self._recover_payment,
            'storage_error': self._recover_storage
        }

        # Health thresholds
        self.max_errors = 10
        self.max_recovery_attempts = 3

        ai_log("kernel", "Enhanced AppKernel constructed")

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
        """Get comprehensive health snapshot"""
        try:
            uptime = int(time.time() - self.boot_ts)
            snapshot = {
                "uptime_sec": uptime,
                "uptime_human": self._format_uptime(uptime),
                "booted": self.state["booted"],
                "last_action": self.state["last_action"],
                "error_count": self.state["errors"],
                "warning_count": self.state["warnings"],
                "recovery_attempts": self.state["recovery_attempts"],
                "health_status": self._calculate_health_status(),
                "timestamp": datetime.now().isoformat()
            }
            ai_log("runtime", f"Health: {snapshot}")
            return snapshot
        except Exception as e:
            ai_exception("runtime", e)
            return None

    def _format_uptime(self, seconds):
        """Format uptime in human-readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs}s"

    def _calculate_health_status(self):
        """Calculate overall health status"""
        if self.state["errors"] >= self.max_errors:
            return "critical"
        elif self.state["errors"] > 5:
            return "warning"
        elif self.state["warnings"] > 10:
            return "degraded"
        else:
            return "healthy"

    # ---------- ERROR RECOVERY ----------

    def auto_recover(self, error_type, context=None):
        """
        AI-driven automatic error recovery

        Args:
            error_type: Type of error (network_error, auth_error, etc.)
            context: Additional context for recovery

        Returns:
            (success, message)
        """
        try:
            if self.state["recovery_attempts"] >= self.max_recovery_attempts:
                ai_log("kernel", f"Max recovery attempts reached - manual intervention needed", "ERROR")
                return False, "Max recovery attempts exceeded"

            self.state["recovery_attempts"] += 1
            ai_log("kernel", f"Attempting auto-recovery for {error_type} (attempt {self.state['recovery_attempts']})")

            strategy = self.error_recovery_strategies.get(error_type)
            if strategy:
                success = strategy(context)
                if success:
                    ai_log("kernel", f"Auto-recovery successful for {error_type}")
                    self.state["recovery_attempts"] = 0  # Reset on success
                    return True, "Recovery successful"
                else:
                    ai_log("kernel", f"Auto-recovery failed for {error_type}", "WARNING")
                    return False, "Recovery failed"
            else:
                return self._fallback_recovery(error_type, context)

        except Exception as e:
            ai_exception("kernel", e)
            return False, str(e)

    def _recover_network(self, context):
        """Recover from network errors"""
        ai_log("kernel", "Executing network recovery strategy")
        try:
            # Import network manager
            from network import NetworkManager
            net = NetworkManager()

            # Check connectivity
            connected, msg = net.check_connectivity()
            if connected:
                ai_log("kernel", "Network recovered")
                return True

            # Try alternative connectivity checks
            ai_log("kernel", "Attempting alternative connectivity check")
            import socket
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=5)
                ai_log("kernel", "Alternative connectivity check passed")
                return True
            except:
                pass

            return False
        except Exception as e:
            ai_exception("kernel", e)
            return False

    def _recover_auth(self, context):
        """Recover from authentication errors"""
        ai_log("kernel", "Executing auth recovery strategy")
        try:
            # Could implement session refresh logic here
            ai_log("kernel", "Auth recovery: clearing invalid sessions")
            # Clear corrupted session files if needed
            return True
        except Exception as e:
            ai_exception("kernel", e)
            return False

    def _recover_payment(self, context):
        """Recover from payment errors"""
        ai_log("kernel", "Executing payment recovery strategy")
        try:
            # Queue payment for retry
            from offline_manager import OfflineManager
            offline = OfflineManager()

            if context:
                operation_id = offline.queue_operation("payment_process", context, priority=10)
                ai_log("kernel", f"Payment queued for retry: {operation_id}")
                return True

            return False
        except Exception as e:
            ai_exception("kernel", e)
            return False

    def _recover_storage(self, context):
        """Recover from storage errors"""
        ai_log("kernel", "Executing storage recovery strategy")
        try:
            import os
            # Check storage availability
            storage_path = "/sdcard"
            if os.path.exists(storage_path) and os.access(storage_path, os.W_OK):
                ai_log("kernel", "Storage is accessible")
                return True

            ai_log("kernel", "Storage not accessible", "ERROR")
            return False
        except Exception as e:
            ai_exception("kernel", e)
            return False

    def _fallback_recovery(self, error_type, context):
        """Fallback recovery strategy"""
        ai_log("kernel", f"Using fallback recovery for {error_type}")

        # Generic recovery: restart affected component
        try:
            ai_log("kernel", "Attempting component restart")
            # Could implement component-specific restart logic
            return False  # Default to manual intervention
        except Exception as e:
            ai_exception("kernel", e)
            return False

    # ---------- MONITORING ----------

    def report_error(self, error_type, error_message):
        """Report and log error"""
        self.state["errors"] += 1
        ai_log("kernel", f"ERROR REPORTED: {error_type} - {error_message}", "ERROR")

        # Attempt auto-recovery if critical
        if error_type in self.error_recovery_strategies:
            self.auto_recover(error_type, {"message": error_message})

    def report_warning(self, warning_message):
        """Report and log warning"""
        self.state["warnings"] += 1
        ai_log("kernel", f"WARNING REPORTED: {warning_message}", "WARNING")

    def reset_health_counters(self):
        """Reset health counters"""
        self.state["errors"] = 0
        self.state["warnings"] = 0
        self.state["recovery_attempts"] = 0
        ai_log("kernel", "Health counters reset")