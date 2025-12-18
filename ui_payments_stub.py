# ui_payments_stub.py
# BRANCH: main
# ROLE: Payments UI stub (FEATURE-GATED)

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class PaymentsStub(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(
            Label(text="Payments are currently unavailable.")
        )
