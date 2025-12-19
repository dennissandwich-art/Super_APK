# permission_gate.py
# BRANCH: main
# ROLE: Permission gating (ANDROID-SAFE, READ-ONLY)

"""
RULES:
- No permission requests
- No Android APIs
- Pure policy checks only
"""

# Default policy: nothing is required at startup
REQUIRES_INTERNET = False
REQUIRES_BILLING = False
REQUIRES_STORAGE = False


def can_start() -> bool:
    # Startup must be allowed without permissions
    return True
