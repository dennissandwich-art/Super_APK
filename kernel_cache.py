# kernel_cache.py
# BRANCH: main
# ROLE: Kernel cache binding (SAFE)

from cache_memory import MemoryCache

class KernelCache:
    def __init__(self):
        self.cache = MemoryCache()

    def get(self, key, default=None):
        return self.cache.get(key, default)

    def set(self, key, value):
        self.cache.set(key, value)
