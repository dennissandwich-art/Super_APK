# backend/auth/telegram_verifier.py
# ROLE: Telegram hash verification (CANONICAL CRYPTO SPEC)

"""
TELEGRAM LOGIN VERIFICATION:
1. Remove hash from payload
2. Sort fields alphabetically
3. Build data_check_string (key=value\n)
4. secret_key = SHA256(BOT_TOKEN)
5. calculated_hash = HMAC_SHA256(secret_key, data_check_string)
6. Compare calculated_hash == received_hash
7. Validate auth_date freshness
"""

import hashlib
import hmac
import time
from typing import Optional


class TelegramVerifier:
    def __init__(self, bot_token: str, max_age_seconds: int = 86400):
        self._secret_key = hashlib.sha256(bot_token.encode()).digest()
        self._max_age = max_age_seconds

    def verify(self, payload: dict) -> bool:
        """
        Verify Telegram login payload.
        Returns True if valid, False otherwise.
        """
        # Step 1: Extract and remove hash
        received_hash = payload.get("hash")
        if not received_hash:
            return False

        # Step 2: Build data_check_string (sorted, without hash)
        data_check_string = self._build_data_check_string(payload)
        if data_check_string is None:
            return False

        # Step 3: Calculate expected hash
        calculated_hash = self._calculate_hash(data_check_string)

        # Step 4: Compare hashes (constant-time)
        if not hmac.compare_digest(calculated_hash, received_hash):
            return False

        # Step 5: Validate auth_date freshness
        if not self._validate_auth_date(payload.get("auth_date")):
            return False

        return True

    def _build_data_check_string(self, payload: dict) -> Optional[str]:
        """Build sorted key=value string, excluding hash."""
        try:
            fields = []
            for key, value in sorted(payload.items()):
                if key == "hash":
                    continue
                if value is not None:
                    fields.append(f"{key}={value}")
            return "\n".join(fields)
        except Exception:
            return None

    def _calculate_hash(self, data_check_string: str) -> str:
        """Calculate HMAC-SHA256 hash."""
        return hmac.new(
            self._secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

    def _validate_auth_date(self, auth_date) -> bool:
        """Check if auth_date is within max_age."""
        try:
            auth_timestamp = int(auth_date)
            current_time = int(time.time())
            return (current_time - auth_timestamp) <= self._max_age
        except (TypeError, ValueError):
            return False
