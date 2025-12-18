# error_boundary.py
# BRANCH: main
# ROLE: Centralized error containment (APP-SAFE)

"""
RULES:
- No imports except standard library
- No UI, no network
- Errors are captured, not raised
"""

class ErrorBoundary:
    def __init__(self):
        self.errors = []

    def capture(self, error: Exception, context: str = ""):
        entry = {
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
        }
        self.errors.append(entry)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def get_errors(self):
        return list(self.errors)
