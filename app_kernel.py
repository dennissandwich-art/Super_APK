# app_kernel.py
# BRANCH: main
# ROLE: Core application kernel (LOGIC ONLY)

"""
RULES:
- No UI imports
- No network
- No Stripe
- No side effects on import
- Deterministic behavior only
"""

from feature_flags import (
    FEATURE_ANALYTICS,
    FEATURE_STRIPE,
    FEATURE_NETWORK,
    FEATURE_DEBUG,
)


class AppKernel:
    def __init__(self):
        self.state = {}

    def initialize(self):
        """
        Initializes internal state.
        Must be safe to call multiple times.
        """
        self.state["initialized"] = True

    def is_feature_enabled(self, feature_name: str) -> bool:
        return bool(globals().get(feature_name, False))
