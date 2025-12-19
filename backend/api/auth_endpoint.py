# backend/api/auth_endpoint.py
# ROLE: POST /auth/telegram endpoint (SINGLE PURPOSE)

"""
API CONTRACT:

POST /auth/telegram

Input:
{
    "id": number,
    "username": string?,
    "first_name": string?,
    "last_name": string?,
    "auth_date": number,
    "hash": string
}

Output (success):
{
    "ok": true,
    "token": "opaque-session-token",
    "expires_in": 86400
}

Output (fail):
{
    "ok": false
}

NO error codes. NO debug info. NO enumeration vectors.
"""

from typing import Optional
from pydantic import BaseModel


class TelegramLoginPayload(BaseModel):
    id: int
    hash: str
    auth_date: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class AuthResponse(BaseModel):
    ok: bool
    token: Optional[str] = None
    expires_in: Optional[int] = None


def create_auth_handler(verifier, session_manager, user_store):
    """
    Factory function to create auth handler with dependencies.
    Returns handler function for use with FastAPI/Flask.
    """

    def handle_telegram_auth(payload: TelegramLoginPayload) -> AuthResponse:
        # Step 1: Validate payload schema (done by Pydantic)

        # Step 2: Convert to dict for verification
        payload_dict = {
            "id": payload.id,
            "hash": payload.hash,
            "auth_date": payload.auth_date,
        }
        if payload.username:
            payload_dict["username"] = payload.username
        if payload.first_name:
            payload_dict["first_name"] = payload.first_name
        if payload.last_name:
            payload_dict["last_name"] = payload.last_name
        if payload.photo_url:
            payload_dict["photo_url"] = payload.photo_url

        # Step 3: Verify Telegram hash
        if not verifier.verify(payload_dict):
            return AuthResponse(ok=False)

        # Step 4: Upsert user
        if not user_store.upsert_user(payload.id, payload.username):
            return AuthResponse(ok=False)

        # Step 5: Generate session token
        session = session_manager.create_session(payload.id)

        # Step 6: Return success response
        return AuthResponse(
            ok=True,
            token=session["token"],
            expires_in=session["expires_in"]
        )

    return handle_telegram_auth
