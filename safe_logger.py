# safe_logger.py
# BRANCH: main
# ROLE: In-memory logger (NO FILE I/O, NO NETWORK)

"""
RULES:
- Logs stay in memory
- No disk writes
- No network
"""

class SafeLogger:
    def __init__(self, limit: int = 200):
        self.limit = limit
        self.buffer = []

    def log(self, message: str):
        if len(self.buffer) >= self.limit:
            self.buffer.pop(0)
        self.buffer.append(message)

    def dump(self):
        return list(self.buffer)
