# app_kernel.py
# BRANCH: main
# ROLE: Core application kernel (FINAL, LOCKED)

from kernel_state import KernelState
from error_boundary import ErrorBoundary
from safe_logger import SafeLogger
from kernel_boot import build_feature_snapshot


class AppKernel:
    def __init__(self):
        self.state = KernelState()
        self.errors = ErrorBoundary()
        self.logger = SafeLogger()
        self.features = None

    def initialize(self):
        try:
            self.features = build_feature_snapshot()
            self.state.mark_initialized()
            self.logger.log("Kernel initialized with feature snapshot")
        except Exception as e:
            self.errors.capture(e, context="kernel.initialize")

    def is_feature_enabled(self, feature_name: str) -> bool:
        if not self.features:
            return False
        return self.features.enabled(feature_name)
