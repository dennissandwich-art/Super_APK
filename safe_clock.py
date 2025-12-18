# safe_clock.py
# BRANCH: main
# ROLE: Read-only time access (SAFE)

import time


def now_seconds() -> float:
    return time.time()
