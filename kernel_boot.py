# kernel_boot.py
# BRANCH: main
# ROLE: Deterministic kernel boot sequence

from feature_flags import (
    FEATURE_ANALYTICS,
    FEATURE_STRIPE,
    FEATURE_NETWORK,
    FEATURE_DEBUG,
)

from kernel_features import KernelFeatures


def build_feature_snapshot() -> KernelFeatures:
    flags = {
        "FEATURE_ANALYTICS": FEATURE_ANALYTICS,
        "FEATURE_STRIPE": FEATURE_STRIPE,
        "FEATURE_NETWORK": FEATURE_NETWORK,
        "FEATURE_DEBUG": FEATURE_DEBUG,
    }
    return KernelFeatures(flags)
