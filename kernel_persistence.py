# kernel_persistence.py
# BRANCH: main
# ROLE: Kernel persistence binding (SAFE)

from persistence_memory import MemoryPersistence


class KernelPersistence:
    def __init__(self):
        self.backend = MemoryPersistence()

    def save_state(self, key: str, value):
        self.backend.save(key, value)

    def load_state(self, key: str, default=None):
        return self.backend.load(key, default)
