# task_queue.py
# BRANCH: main
# ROLE: Deterministic task queue (NO THREADS, NO TIMERS)

"""
RULES:
- No threading
- No async
- Tasks executed explicitly
"""

class TaskQueue:
    def __init__(self):
        self._queue = []

    def add(self, fn, *args, **kwargs):
        self._queue.append((fn, args, kwargs))

    def run_all(self):
        while self._queue:
            fn, args, kwargs = self._queue.pop(0)
            fn(*args, **kwargs)
