# feature_audit.py
# BRANCH: main
# ROLE: Feature audit snapshot

from feature_registry import FEATURES

def audit():
    return {k: v.get("default") for k, v in FEATURES.items()}
