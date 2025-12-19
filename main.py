# main.py
# BRANCH: main
# ROLE: UI ENTRYPOINT (LOGIN FLOW INTEGRATED)

"""
EARLY PHASE MAIN:
1. Show login screen
2. Handle Telegram login
3. Show result
4. No other features
"""

from kivy.app import App

from app_kernel import AppKernel
from lifecycle_hooks import LifecycleHooks
from kernel_events import KernelEvents
from kernel_ready import emit_ready
from ui_router import UIRouter
from ui_events import UIEvents
from ui_login import LoginState
from telegram_login_handler import TelegramLoginHandler


class SuperAPKApp(App):
    def build(self):
        # Core components
        self.kernel = AppKernel()
        self.lifecycle = LifecycleHooks()
        self.events = KernelEvents()
        self.router = UIRouter()

        # Event bindings
        self.ui_events = UIEvents(self.events)
        self.ui_events.bind()

        # Login handler (backend URL configurable)
        self.login_handler = TelegramLoginHandler(
            backend_url="http://localhost:8000"
        )
        self.login_handler.set_state_callback(self._on_login_state_change)

        # Wire up login button
        self.router.set_login_callback(self._on_login_request)

        # Initialize kernel
        self.kernel.initialize()
        emit_ready(self.events)

        # Start with login screen
        return self.router.route_initial()

    def _on_login_request(self):
        """Called when user taps Login button."""
        self.router.set_login_state(LoginState.LOGGING_IN)
        self.login_handler.initiate_login()

    def _on_login_state_change(self, state: str):
        """Called when login state changes."""
        self.router.set_login_state(state)

    def on_telegram_payload(self, payload: dict):
        """
        Called when Telegram returns login payload.
        In production: called from WebView/intent callback.
        """
        success = self.login_handler.handle_telegram_response(payload)
        if success:
            # Could route to main app here
            pass

    def on_pause(self):
        self.lifecycle.on_pause()
        return True

    def on_resume(self):
        self.lifecycle.on_resume()

    def on_stop(self):
        self.lifecycle.on_stop()


if __name__ == "__main__":
    SuperAPKApp().run()
