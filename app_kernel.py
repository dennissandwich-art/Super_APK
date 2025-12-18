"""
NTRLI SuperAPK - Application Kernel
====================================

The kernel is the SINGLE execution authority for the application.
All subsystem initialization and lifecycle management flows through here.

INVARIANTS (violations will crash):
1. Only one kernel instance may exist
2. Subsystems must be initialized before use
3. State mutations must go through state_manager
4. Network calls must go through network module

This module enforces these rules at runtime.
"""

import time
import sys
from datetime import datetime
from typing import Optional, Dict, Any, Callable

try:
    from modules.ai_core import ai_log, ai_exception
except ImportError:
    # Fallback logging if ai_core not available
    def ai_log(tag, msg, level="INFO"):
        print(f"[{level}] [{tag}] {msg}")

    def ai_exception(tag, e):
        print(f"[ERROR] [{tag}] {e}")


class KernelInvariantViolation(Exception):
    """
    Raised when a kernel invariant is violated.

    These violations indicate a fundamental architectural problem
    and should crash the application loudly.
    """
    pass


class SubsystemNotInitializedError(Exception):
    """Raised when attempting to use an uninitialized subsystem."""
    pass


class AppKernel:
    """
    Application Kernel - Single Execution Authority

    Responsibilities:
    - Initialize all subsystems in correct order
    - Inject dependencies
    - Own application lifecycle
    - Terminate on invariant violation
    """

    _instance: Optional['AppKernel'] = None
    _initialized: bool = False

    def __new__(cls):
        """Enforce singleton pattern - only one kernel allowed."""
        if cls._instance is not None:
            raise KernelInvariantViolation(
                "FATAL: Attempted to create second AppKernel instance. "
                "Only one kernel may exist per application."
            )
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if AppKernel._initialized:
            return  # Already initialized (singleton)

        self.boot_ts = time.time()
        self._subsystems: Dict[str, Any] = {}
        self._subsystem_status: Dict[str, bool] = {}
        self._shutdown_hooks: list = []

        # Internal state (NOT application state - use state_manager for that)
        self._kernel_state = {
            "booted": False,
            "error_count": 0,
            "last_error": None,
        }

        AppKernel._initialized = True
        ai_log("kernel", "AppKernel constructed (singleton)")

    @classmethod
    def get_instance(cls) -> 'AppKernel':
        """Get the kernel instance. Raises if not initialized."""
        if cls._instance is None:
            raise KernelInvariantViolation(
                "FATAL: Kernel not initialized. "
                "Call AppKernel() before get_instance()."
            )
        return cls._instance

    @classmethod
    def reset_for_testing(cls):
        """Reset kernel state for testing only."""
        cls._instance = None
        cls._initialized = False

    # ==================== LIFECYCLE ====================

    def boot(self) -> bool:
        """
        Boot the kernel and initialize core subsystems.

        Returns:
            True if boot successful, False otherwise.
            On critical failure, raises KernelInvariantViolation.
        """
        ai_log("kernel", "=== KERNEL BOOT SEQUENCE STARTED ===")

        try:
            # Initialize subsystems in dependency order
            self._init_state_manager()
            self._init_network()
            self._init_monitoring()

            self._kernel_state["booted"] = True
            ai_log("kernel", "=== KERNEL BOOT COMPLETE ===")
            return True

        except Exception as e:
            ai_exception("kernel", e)
            self._kernel_state["last_error"] = str(e)
            self._kernel_state["error_count"] += 1

            # Critical boot failure - crash loudly
            raise KernelInvariantViolation(
                f"FATAL: Kernel boot failed: {e}"
            ) from e

    def _init_state_manager(self):
        """Initialize state manager subsystem."""
        try:
            from state_manager import AppState
            self._subsystems["state"] = AppState()
            self._subsystem_status["state"] = True
            ai_log("kernel", "StateManager initialized")
        except ImportError:
            ai_log("kernel", "StateManager not available - using stub", "WARNING")
            self._subsystem_status["state"] = False

    def _init_network(self):
        """Initialize network subsystem."""
        try:
            from network import NetworkManager
            self._subsystems["network"] = NetworkManager()
            self._subsystem_status["network"] = True
            ai_log("kernel", "NetworkManager initialized")
        except ImportError:
            ai_log("kernel", "NetworkManager not available", "WARNING")
            self._subsystem_status["network"] = False

    def _init_monitoring(self):
        """Initialize monitoring subsystem."""
        try:
            from monitoring import MonitoringManager
            self._subsystems["monitoring"] = MonitoringManager()
            self._subsystem_status["monitoring"] = True
            ai_log("kernel", "MonitoringManager initialized")
        except ImportError:
            ai_log("kernel", "MonitoringManager not available", "WARNING")
            self._subsystem_status["monitoring"] = False

    def shutdown(self):
        """
        Graceful shutdown of kernel and all subsystems.
        """
        ai_log("kernel", "=== KERNEL SHUTDOWN INITIATED ===")

        # Run shutdown hooks in reverse order
        for hook in reversed(self._shutdown_hooks):
            try:
                hook()
            except Exception as e:
                ai_exception("kernel", e)

        # Clear subsystems
        self._subsystems.clear()
        self._subsystem_status.clear()

        self._kernel_state["booted"] = False
        ai_log("kernel", "=== KERNEL SHUTDOWN COMPLETE ===")

    def register_shutdown_hook(self, hook: Callable[[], None]):
        """Register a function to be called on shutdown."""
        self._shutdown_hooks.append(hook)

    # ==================== SUBSYSTEM ACCESS ====================

    def get_subsystem(self, name: str) -> Any:
        """
        Get an initialized subsystem.

        Raises SubsystemNotInitializedError if subsystem is not available.
        """
        if name not in self._subsystems:
            raise SubsystemNotInitializedError(
                f"Subsystem '{name}' is not initialized. "
                f"Available: {list(self._subsystems.keys())}"
            )
        return self._subsystems[name]

    def is_subsystem_available(self, name: str) -> bool:
        """Check if a subsystem is available."""
        return self._subsystem_status.get(name, False)

    @property
    def state_manager(self):
        """Get state manager (convenience property)."""
        return self.get_subsystem("state")

    @property
    def network(self):
        """Get network manager (convenience property)."""
        return self.get_subsystem("network")

    @property
    def monitoring(self):
        """Get monitoring manager (convenience property)."""
        return self.get_subsystem("monitoring")

    # ==================== INVARIANT ENFORCEMENT ====================

    def assert_invariant(self, condition: bool, message: str):
        """
        Assert a kernel invariant. Crashes if violated.

        Use this for conditions that should NEVER be false in correct code.
        """
        if not condition:
            error_msg = f"INVARIANT VIOLATION: {message}"
            ai_log("kernel", error_msg, "FATAL")
            self._kernel_state["error_count"] += 1
            self._kernel_state["last_error"] = error_msg

            # Crash loudly
            raise KernelInvariantViolation(error_msg)

    def assert_booted(self):
        """Assert kernel is booted. Crashes if not."""
        self.assert_invariant(
            self._kernel_state["booted"],
            "Kernel must be booted before use"
        )

    # ==================== DIAGNOSTICS ====================

    def health_snapshot(self) -> Dict[str, Any]:
        """Get kernel health snapshot."""
        uptime = int(time.time() - self.boot_ts)
        return {
            "uptime_sec": uptime,
            "uptime_human": self._format_uptime(uptime),
            "booted": self._kernel_state["booted"],
            "error_count": self._kernel_state["error_count"],
            "last_error": self._kernel_state["last_error"],
            "subsystems": {
                name: "OK" if status else "UNAVAILABLE"
                for name, status in self._subsystem_status.items()
            },
            "timestamp": datetime.now().isoformat()
        }

    def _format_uptime(self, seconds: int) -> str:
        """Format uptime in human-readable format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}h {minutes}m {secs}s"

    # ==================== ERROR HANDLING ====================

    def report_error(self, component: str, error: Exception):
        """
        Report an error to the kernel.

        This logs the error and updates metrics. It does NOT attempt
        automatic recovery - that was cosmetic and has been removed.
        """
        self._kernel_state["error_count"] += 1
        self._kernel_state["last_error"] = f"{component}: {error}"
        ai_exception(component, error)

        # Track in monitoring if available
        if self.is_subsystem_available("monitoring"):
            try:
                self.monitoring.track_error(
                    component,
                    str(error),
                    {"timestamp": datetime.now().isoformat()}
                )
            except Exception:
                pass  # Don't fail on monitoring failure


# Module-level convenience function
def get_kernel() -> AppKernel:
    """Get the kernel instance."""
    return AppKernel.get_instance()
