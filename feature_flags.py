# feature_flags.py
# BRANCH: main
# ROLE: Central feature gating (PLATFORM SAFE)

"""
This file contains ONLY boolean flags.
No imports.
No logic.
No side effects.

Main may reference this file safely.
Optional modules may read from it.
"""

# Core platform flags
FEATURE_ANALYTICS = False
FEATURE_STRIPE = False
FEATURE_NETWORK = False
FEATURE_DEBUG = False
