# event_bus.py
# BRANCH: main
# ROLE: Simple synchronous event bus (NO ASYNC)

"""
RULES:
- No threading
- No async
- Handlers run immediately
"""

class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event_name: str, handler):
        self._handlers.setdefault(event_name, []).append(handler)

    def emit(self, event_name: str, payload=None):
        for handler in self._handlers.get(event_name, []):
            handler(payload)
