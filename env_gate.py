# env_gate.py
# BRANCH: main
# ROLE: Environment gating (BUILD-TIME SAFE)

"""
RULES:
- No os.environ writes
- Read-only access
- Safe defaults if unavailable
"""

def get_env_flag(name: str, default: bool = False) -> bool:
    try:
        import os
        value = os.environ.get(name)
        if value is None:
            return default
        return value.lower() in ("1", "true", "yes", "on")
    except Exception:
        return default
