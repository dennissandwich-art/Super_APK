# kernel_events.py
# BRANCH: main
# ROLE: Kernel event integration

from event_bus import EventBus


class KernelEvents:
    def __init__(self):
        self.bus = EventBus()

    def emit(self, name: str, payload=None):
        self.bus.emit(name, payload)

    def on(self, name: str, handler):
        self.bus.on(name, handler)
