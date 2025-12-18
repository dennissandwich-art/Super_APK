# ui_heartbeat.py
# BRANCH: main
# ROLE: UI heartbeat indicator (PASSIVE)

from kivy.uix.label import Label
from uptime import Uptime


class Heartbeat(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uptime = Uptime()
        self.text = "Alive"

    def update(self):
        # Optional manual update
        self.text = f"Uptime: {int(self.uptime.seconds())}s"
