# main.py
# BRANCH: main
# ROLE: UI ENTRYPOINT (PLATFORM SAFE)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from app_kernel import AppKernel


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
        self.kernel = AppKernel()
        self.kernel.initialize()
        return RootLayout()


if __name__ == "__main__":
    SuperAPKApp().run()
