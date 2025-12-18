# app_kernel.py
# BRANCH: main
# ROLE: Core application kernel (LOGIC ONLY)

from feature_flags import (
    FEATURE_ANALYTICS,
    FEATURE_STRIPE,
    FEATURE_NETWORK,
    FEATURE_DEBUG,
)

from kernel_state import KernelState
from error_boundary import ErrorBoundary
from safe_logger import SafeLogger


class AppKernel:
    def __init__(self):
        self.state = KernelState()
        self.errors = ErrorBoundary()
        self.logger = SafeLogger()

    def initialize(self):
        try:
            self.state.mark_initialized()
            self.state.features_enabled = {
                "FEATURE_ANALYTICS": FEATURE_ANALYTICS,
                "FEATURE_STRIPE": FEATURE_STRIPE,
                "FEATURE_NETWORK": FEATURE_NETWORK,
                "FEATURE_DEBUG": FEATURE_DEBUG,
            }
            self.logger.log("Kernel initialized")
        except Exception as e:
            self.errors.capture(e, context="kernel.initialize")

    def is_feature_enabled(self, feature_name: str) -> bool:
        return self.state.features_enabled.get(feature_name, False)
