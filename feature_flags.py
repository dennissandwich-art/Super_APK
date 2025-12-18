# feature_flags.py
# BRANCH: main
# ROLE: Central feature gating (ENV AWARE, SAFE)

from env_gate import get_env_flag

FEATURE_ANALYTICS = get_env_flag("FEATURE_ANALYTICS", False)
FEATURE_STRIPE = get_env_flag("FEATURE_STRIPE", False)
FEATURE_NETWORK = get_env_flag("FEATURE_NETWORK", False)
FEATURE_DEBUG = get_env_flag("FEATURE_DEBUG", False)
