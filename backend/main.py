# backend/main.py
# ROLE: Auth Gateway entrypoint (FastAPI)

"""
BACKEND ROLE: Auth Gateway only.
NOT: user service, business logic, data hub.

Single endpoint: POST /auth/telegram
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.env_contract import EnvContract
from auth.telegram_verifier import TelegramVerifier
from auth.session_manager import SessionManager
from store.user_store import UserStore
from api.auth_endpoint import TelegramLoginPayload, AuthResponse, create_auth_handler


# Initialize app
app = FastAPI(
    title="Super_APK Auth Gateway",
    description="Telegram login verification + session token",
    version="1.0.0",
    docs_url=None,  # Disable docs in production
    redoc_url=None
)

# CORS (restrictive)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_methods=["POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Initialize components
try:
    _bot_token = EnvContract.get_bot_token()
    _session_ttl = EnvContract.get_session_ttl()
    _db_path = EnvContract.get_database_path()

    _verifier = TelegramVerifier(_bot_token, max_age_seconds=86400)
    _session_manager = SessionManager(ttl_seconds=_session_ttl)
    _user_store = UserStore(db_path=_db_path)

    _auth_handler = create_auth_handler(_verifier, _session_manager, _user_store)
    _initialized = True
except EnvironmentError:
    _initialized = False
    _auth_handler = None


@app.post("/auth/telegram", response_model=AuthResponse)
async def auth_telegram(payload: TelegramLoginPayload) -> AuthResponse:
    """
    Telegram login verification endpoint.

    Returns ok=true with token on success.
    Returns ok=false on any failure (no details).
    """
    if not _initialized or _auth_handler is None:
        return AuthResponse(ok=False)

    try:
        return _auth_handler(payload)
    except Exception:
        # Never expose internal errors
        return AuthResponse(ok=False)


@app.get("/health")
async def health():
    """Health check (minimal)."""
    return {"status": "ok" if _initialized else "not_configured"}
