# watchdog.py
# BRANCH: main
# ROLE: Simple watchdog (PASSIVE)

import time


class Watchdog:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds
        self.start_time = time.time()

    def expired(self) -> bool:
        return (time.time() - self.start_time) > self.timeout

    def reset(self):
        self.start_time = time.time()
