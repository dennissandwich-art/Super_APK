# main.py
# BRANCH: main
# ROLE: UI ENTRYPOINT (BOOT-FIRST, PLATFORM SAFE)

from kivy.app import App

from app_kernel import AppKernel
from ui_router import UIRouter
from lifecycle_hooks import LifecycleHooks


class SuperAPKApp(App):
    def build(self):
        self.kernel = AppKernel()
        self.lifecycle = LifecycleHooks()
        self.router = UIRouter()

        # Kernel init must NEVER block UI
        self.kernel.initialize()

        # UI boots immediately
        return self.router.route_initial()

    def on_pause(self):
        self.lifecycle.on_pause()
        return True

    def on_resume(self):
        self.lifecycle.on_resume()

    def on_stop(self):
        self.lifecycle.on_stop()


if __name__ == "__main__":
    SuperAPKApp().run()
