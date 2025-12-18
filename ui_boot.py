# ui_boot.py
# BRANCH: main
# ROLE: Minimal boot UI (SAFE, NO ASSETS)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class BootScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(
            Label(
                text="Starting Super_APK…",
                halign="center",
                valign="middle"
            )
        )
