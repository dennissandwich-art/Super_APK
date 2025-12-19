# ui_events.py
# BRANCH: main
# ROLE: UI event bindings

class UIEvents:
    def __init__(self, kernel_events):
        self.events = kernel_events

    def bind(self):
        self.events.on("kernel_ready", self.on_kernel_ready)

    def on_kernel_ready(self, payload):
        pass
