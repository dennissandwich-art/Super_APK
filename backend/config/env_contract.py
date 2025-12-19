# backend/config/env_contract.py
# ROLE: Environment contract (REQUIRED/OPTIONAL)

"""
ENVIRONMENT CONTRACT:
- TELEGRAM_BOT_TOKEN: REQUIRED (no default)
- SESSION_TTL_SECONDS: OPTIONAL (default 86400)
- DATABASE_PATH: OPTIONAL (default ./data/users.db)
"""

import os


class EnvContract:
    @staticmethod
    def get_bot_token() -> str:
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            raise EnvironmentError("TELEGRAM_BOT_TOKEN is REQUIRED")
        return token

    @staticmethod
    def get_session_ttl() -> int:
        return int(os.environ.get("SESSION_TTL_SECONDS", "86400"))

    @staticmethod
    def get_database_path() -> str:
        return os.environ.get("DATABASE_PATH", "./data/users.db")
