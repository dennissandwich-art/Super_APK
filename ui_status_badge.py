# ui_status_badge.py
# BRANCH: main
# ROLE: UI status badge (OFFLINE)

from kivy.uix.label import Label

class StatusBadge(Label):
    def __init__(self, status: str = "OK", **kwargs):
        super().__init__(**kwargs)
        self.text = f"Status: {status}"

    def set_status(self, status: str):
        self.text = f"Status: {status}"
