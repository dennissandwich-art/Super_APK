# id_generator.py
# BRANCH: main
# ROLE: Deterministic ID generator (NO RNG)

class IdGenerator:
    def __init__(self):
        self._next = 1

    def next_id(self) -> int:
        value = self._next
        self._next += 1
        return value
