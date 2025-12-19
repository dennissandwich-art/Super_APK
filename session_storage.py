# session_storage.py
# BRANCH: main
# ROLE: Session token storage (ANDROID SIDE, SIMPLE)

"""
SESSION STORAGE SPEC:
- Store session token temporarily
- Memory-only in early phase (acceptable)
- App restart = re-login required

NO:
- Persistent storage (yet)
- Token refresh
- Complex caching
"""


class SessionStorage:
    def __init__(self):
        self._token = None
        self._expires_in = None

    def store(self, token: str, expires_in: int = None):
        """Store session token."""
        self._token = token
        self._expires_in = expires_in

    def get_token(self) -> str:
        """Get current token. Returns None if not set."""
        return self._token

    def clear(self):
        """Clear stored session."""
        self._token = None
        self._expires_in = None

    def has_session(self) -> bool:
        """Check if session exists."""
        return self._token is not None
