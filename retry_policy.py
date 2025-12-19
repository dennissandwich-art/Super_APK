# retry_policy.py
# BRANCH: main
# ROLE: Retry policy (NO TIMERS)

class RetryPolicy:
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def run(self, fn, *args, **kwargs):
        attempts = 0
        while attempts < self.max_attempts:
            try:
                return fn(*args, **kwargs)
            except Exception:
                attempts += 1
        return None
