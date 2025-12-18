# uptime.py
# BRANCH: main
# ROLE: App uptime tracker (SAFE)

from safe_clock import now_seconds


class Uptime:
    def __init__(self):
        self.start = now_seconds()

    def seconds(self) -> float:
        return now_seconds() - self.start
