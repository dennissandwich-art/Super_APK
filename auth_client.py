# auth_client.py
# BRANCH: main
# ROLE: Backend auth client (ANDROID SIDE)

"""
AUTH CLIENT SPEC:
- Send Telegram payload to backend
- Return success/fail
- Handle network errors gracefully

ANDROID MUST NOT:
- Validate hash
- Know BOT_TOKEN
- Assume login is correct
- Bypass backend
"""

import json
from typing import Optional

# Note: In actual Android/Kivy app, use kivy.network.urlrequest
# For now, using urllib for simplicity (works on Android)
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
except ImportError:
    Request = None
    urlopen = None
    URLError = Exception
    HTTPError = Exception


class AuthResult:
    def __init__(self, ok: bool, token: str = None, expires_in: int = None, error: str = None):
        self.ok = ok
        self.token = token
        self.expires_in = expires_in
        self.error = error


class AuthClient:
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self._backend_url = backend_url.rstrip("/")
        self._timeout = 10  # seconds

    def authenticate(self, telegram_payload: dict) -> AuthResult:
        """
        Send Telegram login payload to backend.
        Returns AuthResult with ok=True/False.
        """
        if urlopen is None:
            return AuthResult(ok=False, error="network_unavailable")

        try:
            url = f"{self._backend_url}/auth/telegram"
            data = json.dumps(telegram_payload).encode("utf-8")

            request = Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urlopen(request, timeout=self._timeout) as response:
                response_data = json.loads(response.read().decode("utf-8"))

                if response_data.get("ok"):
                    return AuthResult(
                        ok=True,
                        token=response_data.get("token"),
                        expires_in=response_data.get("expires_in")
                    )
                else:
                    return AuthResult(ok=False, error="access_denied")

        except (URLError, HTTPError):
            return AuthResult(ok=False, error="backend_unavailable")
        except json.JSONDecodeError:
            return AuthResult(ok=False, error="invalid_response")
        except Exception:
            return AuthResult(ok=False, error="unknown_error")
