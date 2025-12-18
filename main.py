# main.py
# BRANCH: main
# ROLE: UI ENTRYPOINT (PLATFORM SAFE)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from app_kernel import AppKernel
from lifecycle_hooks import LifecycleHooks


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
        self.lifecycle = LifecycleHooks()
        self.kernel.initialize()
        return RootLayout()

    def on_pause(self):
        self.lifecycle.on_pause()
        return True

    def on_resume(self):
        self.lifecycle.on_resume()

    def on_stop(self):
        self.lifecycle.on_stop()


if __name__ == "__main__":
    SuperAPKApp().run()
