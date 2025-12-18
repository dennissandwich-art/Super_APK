# ui_debug.py
# BRANCH: main
# ROLE: Optional debug panel (SAFE)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kernel_health import KernelHealth


class DebugPanel(BoxLayout):
    def __init__(self, kernel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        health = KernelHealth(kernel)

        self.add_widget(Label(text=f"Initialized: {health.initialized}"))
        self.add_widget(Label(text=f"Errors: {len(health.errors)}"))
