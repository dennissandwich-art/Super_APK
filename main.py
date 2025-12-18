# main.py
# BRANCH: main
# ROLE: Platform entrypoint (FROZEN)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(
            Label(
                text="Super_APK",
                halign="center",
                valign="middle"
            )
        )


class SuperAPKApp(App):
    def build(self):
        # HARD RULE:
        # - No network calls
        # - No Stripe
        # - No analytics
        # - UI must be first live object
        return RootLayout()


if __name__ == "__main__":
    SuperAPKApp().run()
