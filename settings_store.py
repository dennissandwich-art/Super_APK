# settings_store.py
# BRANCH: main
# ROLE: In-memory settings store (SAFE)

"""
RULES:
- No disk I/O
- No network
- Can be replaced later
"""

class SettingsStore:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value):
        self._store[key] = value

    def get(self, key: str, default=None):
        return self._store.get(key, default)

    def dump(self):
        return dict(self._store)
