# backend/auth/session_manager.py
# ROLE: Session token management (OPAQUE, TIME-LIMITED)

"""
SESSION CONTRACT:
- Token is opaque (random hex)
- Token is time-limited
- Token is bound to tg_user_id
- No refresh tokens
- No JWT
"""

import secrets
import time
from typing import Optional, Dict


class SessionManager:
    def __init__(self, ttl_seconds: int = 86400):
        self._ttl = ttl_seconds
        self._sessions: Dict[str, dict] = {}

    def create_session(self, tg_user_id: int) -> dict:
        """
        Create new session for user.
        Returns: { token, expires_in, expires_at }
        """
        token = secrets.token_hex(32)
        expires_at = int(time.time()) + self._ttl

        self._sessions[token] = {
            "tg_user_id": tg_user_id,
            "expires_at": expires_at
        }

        return {
            "token": token,
            "expires_in": self._ttl,
            "expires_at": expires_at
        }

    def validate_session(self, token: str) -> Optional[int]:
        """
        Validate session token.
        Returns tg_user_id if valid, None otherwise.
        """
        session = self._sessions.get(token)
        if not session:
            return None

        if time.time() > session["expires_at"]:
            # Expired - remove and reject
            del self._sessions[token]
            return None

        return session["tg_user_id"]

    def invalidate_session(self, token: str) -> bool:
        """Invalidate session. Returns True if existed."""
        if token in self._sessions:
            del self._sessions[token]
            return True
        return False

    def cleanup_expired(self) -> int:
        """Remove all expired sessions. Returns count removed."""
        current_time = time.time()
        expired = [
            token for token, data in self._sessions.items()
            if current_time > data["expires_at"]
        ]
        for token in expired:
            del self._sessions[token]
        return len(expired)
