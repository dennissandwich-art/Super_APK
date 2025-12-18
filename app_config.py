# app_config.py
# BRANCH: main
# ROLE: Static configuration defaults (OFFLINE SAFE)

"""
RULES:
- No imports
- No environment access
- No runtime logic
- Values here must be safe defaults
"""

APP_NAME = "Super_APK"
APP_VERSION = "1.0.0"

# Runtime safety defaults
ALLOW_NETWORK_AT_START = False
ALLOW_PAYMENTS_AT_START = False
ALLOW_ANALYTICS_AT_START = False

# UI behavior
DEFAULT_LANGUAGE = "en"
