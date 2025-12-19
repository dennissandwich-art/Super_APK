# cache_memory.py
# BRANCH: main
# ROLE: In-memory cache (SAFE)

class MemoryCache:
    def __init__(self, max_items: int = 128):
        self.max_items = max_items
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        if len(self._data) >= self.max_items:
            self._data.pop(next(iter(self._data)))
        self._data[key] = value

    def clear(self):
        self._data.clear()
