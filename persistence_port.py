# persistence_port.py
# BRANCH: main
# ROLE: Persistence abstraction (NO I/O, NO IMPLEMENTATION)

"""
Defines how persistence MAY be used later.
No disk, no network, no Android APIs here.
"""

class PersistencePort:
    def save(self, key: str, value):
        raise NotImplementedError

    def load(self, key: str, default=None):
        raise NotImplementedError
