# telegram_login_handler.py
# BRANCH: main
# ROLE: Telegram login flow handler (ANDROID SIDE)

"""
TELEGRAM LOGIN HANDLER SPEC:
1. User taps "Login med Telegram"
2. Open Telegram login (WebView / intent)
3. Receive Telegram payload
4. Send to backend
5. Handle response

NOTE: Actual Telegram WebView/intent integration requires
platform-specific code. This handler provides the interface.
"""

from auth_client import AuthClient, AuthResult
from session_storage import SessionStorage


class TelegramLoginHandler:
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self._auth_client = AuthClient(backend_url)
        self._session = SessionStorage()
        self._on_state_change = None

    def set_state_callback(self, callback):
        """Set callback for state changes."""
        self._on_state_change = callback

    def _notify_state(self, state: str):
        if self._on_state_change:
            self._on_state_change(state)

    def initiate_login(self):
        """
        Start Telegram login flow.
        In production: opens Telegram WebView/intent.
        For testing: use simulate_telegram_response().
        """
        self._notify_state("logging_in")
        # Platform-specific: Open Telegram login widget
        # The actual implementation depends on:
        # - Telegram Bot API setup
        # - WebView or external browser intent
        # - Callback URL configuration

    def handle_telegram_response(self, payload: dict) -> bool:
        """
        Handle response from Telegram login.
        Called when Telegram returns payload.
        Returns True if login successful.
        """
        self._notify_state("logging_in")

        # Send to backend
        result = self._auth_client.authenticate(payload)

        if result.ok:
            self._session.store(result.token, result.expires_in)
            self._notify_state("success")
            return True

        elif result.error == "backend_unavailable":
            self._notify_state("backend_down")
            return False

        else:
            self._notify_state("fail")
            return False

    def get_session_token(self) -> str:
        """Get current session token."""
        return self._session.get_token()

    def has_session(self) -> bool:
        """Check if user is logged in."""
        return self._session.has_session()

    def logout(self):
        """Clear session."""
        self._session.clear()
        self._notify_state("idle")

    # --- Testing helpers (not for production) ---

    def simulate_telegram_response(self, user_id: int, username: str = None):
        """
        Simulate Telegram login response for testing.
        In production, this comes from Telegram WebView.
        """
        import time
        import hashlib
        import hmac

        # This creates a FAKE payload for testing UI flow
        # Real hash requires BOT_TOKEN (server-side only)
        payload = {
            "id": user_id,
            "auth_date": int(time.time()),
            "hash": "test_hash_for_ui_testing"
        }
        if username:
            payload["username"] = username

        return self.handle_telegram_response(payload)
