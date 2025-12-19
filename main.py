# main.py
# BRANCH: main
# ROLE: UI ENTRYPOINT (EVENT-WIRED)

from kivy.app import App

from app_kernel import AppKernel
from lifecycle_hooks import LifecycleHooks
from kernel_events import KernelEvents
from kernel_ready import emit_ready
from ui_router import UIRouter
from ui_events import UIEvents


class SuperAPKApp(App):
    def build(self):
        self.kernel = AppKernel()
        self.lifecycle = LifecycleHooks()
        self.events = KernelEvents()
        self.router = UIRouter()

        self.ui_events = UIEvents(self.events)
        self.ui_events.bind()

        self.kernel.initialize()
        emit_ready(self.events)

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
