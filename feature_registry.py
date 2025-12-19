# feature_registry.py
# BRANCH: main
# ROLE: Central feature registry (DATA-ONLY)

"""
FEATURE REGISTRY:
- All features defined here
- Default = OFF
- No side-effects at import
"""

FEATURES = {
    "analytics": {
        "default": False,
        "description": "Usage analytics",
    },
    "stripe": {
        "default": False,
        "description": "Stripe payments",
    },
    "network": {
        "default": False,
        "description": "Network features",
    },
    "debug": {
        "default": False,
        "description": "Debug mode",
    },
    "ai_assistant": {
        "default": False,
        "description": "AI Assistant integration",
    },
    "admin_panel": {
        "default": False,
        "description": "Admin panel access",
    },
}


def get_feature(name: str) -> dict:
    """Get feature config by name."""
    return FEATURES.get(name, {"default": False})


def is_feature_enabled(name: str) -> bool:
    """Check if feature is enabled by default."""
    return FEATURES.get(name, {}).get("default", False)
