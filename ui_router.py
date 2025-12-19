# ui_router.py
# BRANCH: main
# ROLE: Deterministic UI routing (SAFE)

"""
UI ROUTING SPEC:
- Start with Login screen
- Route to Result screen after login
- No complex navigation in early phase
"""

from ui_login import LoginScreen, LoginState
from ui_login_result import LoginResultScreen


class UIRouter:
    def __init__(self):
        self.current = None
        self._login_screen = None
        self._on_login_request = None

    def set_login_callback(self, callback):
        """Set callback for login requests."""
        self._on_login_request = callback

    def route_initial(self):
        """Return initial screen (Login)."""
        self._login_screen = LoginScreen(on_login_request=self._on_login_request)
        self.current = self._login_screen
        return self.current

    def set_login_state(self, state: str):
        """Update login screen state."""
        if self._login_screen:
            self._login_screen.set_state(state)

    def route_to_result(self, success: bool, message: str = None):
        """Route to result screen."""
        self.current = LoginResultScreen(success=success, message=message)
        return self.current
