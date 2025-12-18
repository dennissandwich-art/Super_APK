# persistence_memory.py
# BRANCH: main
# ROLE: In-memory persistence (SAFE DEFAULT)

from persistence_port import PersistencePort


class MemoryPersistence(PersistencePort):
    def __init__(self):
        self._store = {}

    def save(self, key: str, value):
        self._store[key] = value

    def load(self, key: str, default=None):
        return self._store.get(key, default)
