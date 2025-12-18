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


class AppKernel:
    def __init__(self):
        self.state = KernelState()

    def initialize(self):
        """
        Safe initialization.
        Can be called multiple times.
        """
        self.state.mark_initialized()

        self.state.features_enabled = {
            "FEATURE_ANALYTICS": FEATURE_ANALYTICS,
            "FEATURE_STRIPE": FEATURE_STRIPE,
            "FEATURE_NETWORK": FEATURE_NETWORK,
            "FEATURE_DEBUG": FEATURE_DEBUG,
        }

    def is_feature_enabled(self, feature_name: str) -> bool:
        return self.state.features_enabled.get(feature_name, False)
