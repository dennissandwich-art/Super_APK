"""
NTRLI SuperAPK - Secure Storage Module
=======================================

Storage for sensitive data with appropriate security measures.

SECURITY MODEL:
- Uses OS-provided storage mechanisms where available
- Falls back to file-based storage with clear warnings
- Does NOT implement custom cryptography
- Relies on Android Keystore on Android, python-keyring on desktop

IMPORTANT:
- This module does NOT claim to provide "military-grade encryption"
- For true secret management, use a proper secret manager
- API keys should use environment variables or secret managers, not this module
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

try:
    from modules.ai_core import AI_CONSOLE
except ImportError:
    AI_CONSOLE = None


# Storage location - NOT for secrets, just for app data
STORAGE_DIR = "/sdcard/superapk_data"
STORAGE_FILE = "/sdcard/superapk_data/app_storage.json"


class SecureStorageWarning(UserWarning):
    """Warning for insecure storage operations."""
    pass


class SecureStorage:
    """
    Secure storage for application data.

    LIMITATIONS (be honest about what this provides):
    - File-based storage with filesystem permissions
    - No encryption on Android external storage
    - For secrets, use environment variables or keyring

    This is suitable for:
    - User preferences
    - Cached data
    - Non-sensitive application state

    This is NOT suitable for:
    - API keys (use environment variables)
    - Passwords (use keyring)
    - Payment credentials (use secure payment providers)
    """

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self._storage: Dict[str, Any] = {}
        self._keyring_available = self._check_keyring()
        self._ensure_storage_dir()
        self._load_storage()
        self._log("SecureStorage initialized")

    def _log(self, msg: str, level: str = "INFO"):
        """Log message."""
        if self.ai_console:
            self.ai_console.log(f"[STORAGE] {msg}", level)
        elif AI_CONSOLE:
            AI_CONSOLE.log(f"[STORAGE] {msg}", level)
        else:
            print(f"[STORAGE] [{level}] {msg}")

    def _check_keyring(self) -> bool:
        """Check if python-keyring is available."""
        try:
            import keyring
            # Test if keyring backend is functional
            keyring.get_keyring()
            return True
        except Exception:
            return False

    def _ensure_storage_dir(self):
        """Ensure storage directory exists."""
        try:
            Path(STORAGE_DIR).mkdir(parents=True, exist_ok=True)
            # Set restrictive permissions where supported
            try:
                os.chmod(STORAGE_DIR, 0o700)
            except OSError:
                pass  # Not all platforms support chmod
        except Exception as e:
            self._log(f"Error creating storage dir: {e}", "ERROR")

    def _load_storage(self):
        """Load storage from file."""
        try:
            if os.path.exists(STORAGE_FILE):
                with open(STORAGE_FILE, "r") as f:
                    self._storage = json.load(f)
        except Exception as e:
            self._log(f"Error loading storage: {e}", "ERROR")
            self._storage = {}

    def _save_storage(self):
        """Save storage to file."""
        try:
            with open(STORAGE_FILE, "w") as f:
                json.dump(self._storage, f, indent=2)
            # Set restrictive permissions
            try:
                os.chmod(STORAGE_FILE, 0o600)
            except OSError:
                pass
        except Exception as e:
            self._log(f"Error saving storage: {e}", "ERROR")

    # ==================== PUBLIC API ====================

    def store(self, key: str, value: Any, user_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Store a value.

        Args:
            key: Storage key
            value: Value to store (must be JSON-serializable)
            user_id: Optional user ID for user-specific storage

        Returns:
            (success, error_message)
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key
            self._storage[storage_key] = {
                "value": value,
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            }
            self._save_storage()
            self._log(f"Stored: {storage_key}")
            return True, None
        except Exception as e:
            return False, str(e)

    def retrieve(self, key: str, user_id: Optional[str] = None) -> Tuple[Any, Optional[str]]:
        """
        Retrieve a value.

        Args:
            key: Storage key
            user_id: Optional user ID

        Returns:
            (value, error_message)
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key
            if storage_key in self._storage:
                return self._storage[storage_key]["value"], None
            return None, "Key not found"
        except Exception as e:
            return None, str(e)

    def delete(self, key: str, user_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Delete a stored value.

        Args:
            key: Storage key
            user_id: Optional user ID

        Returns:
            (success, error_message)
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key
            if storage_key in self._storage:
                del self._storage[storage_key]
                self._save_storage()
                self._log(f"Deleted: {storage_key}")
                return True, None
            return False, "Key not found"
        except Exception as e:
            return False, str(e)

    def list_keys(self, user_id: Optional[str] = None) -> list:
        """List all stored keys."""
        if user_id:
            prefix = f"{user_id}:"
            return [k.replace(prefix, "") for k in self._storage.keys() if k.startswith(prefix)]
        return list(self._storage.keys())

    def clear_all(self, user_id: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """Clear all stored values (or user-specific)."""
        try:
            if user_id:
                prefix = f"{user_id}:"
                keys_to_delete = [k for k in self._storage.keys() if k.startswith(prefix)]
                for key in keys_to_delete:
                    del self._storage[key]
            else:
                self._storage = {}

            self._save_storage()
            self._log(f"Cleared{' for user ' + user_id if user_id else ''}")
            return True, None
        except Exception as e:
            return False, str(e)

    # ==================== SECRET MANAGEMENT ====================

    def store_secret(self, service: str, key: str, secret: str) -> Tuple[bool, Optional[str]]:
        """
        Store a secret using the system keyring.

        This is the ONLY method that should be used for sensitive credentials.
        Falls back to warning if keyring is not available.

        Args:
            service: Service name (e.g., "superapk")
            key: Secret key (e.g., "stripe_api_key")
            secret: The secret value

        Returns:
            (success, error_message)
        """
        if not self._keyring_available:
            import warnings
            warnings.warn(
                f"python-keyring not available. Secret '{key}' cannot be stored securely. "
                "Install keyring: pip install keyring",
                SecureStorageWarning
            )
            return False, "Keyring not available - cannot store secrets securely"

        try:
            import keyring
            keyring.set_password(service, key, secret)
            self._log(f"Secret stored in keyring: {service}/{key}")
            return True, None
        except Exception as e:
            return False, f"Keyring error: {e}"

    def retrieve_secret(self, service: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieve a secret from the system keyring.

        Args:
            service: Service name
            key: Secret key

        Returns:
            (secret, error_message)
        """
        if not self._keyring_available:
            return None, "Keyring not available"

        try:
            import keyring
            secret = keyring.get_password(service, key)
            if secret:
                self._log(f"Secret retrieved from keyring: {service}/{key}")
                return secret, None
            return None, "Secret not found"
        except Exception as e:
            return None, f"Keyring error: {e}"

    def delete_secret(self, service: str, key: str) -> Tuple[bool, Optional[str]]:
        """
        Delete a secret from the system keyring.

        Args:
            service: Service name
            key: Secret key

        Returns:
            (success, error_message)
        """
        if not self._keyring_available:
            return False, "Keyring not available"

        try:
            import keyring
            keyring.delete_password(service, key)
            self._log(f"Secret deleted from keyring: {service}/{key}")
            return True, None
        except Exception as e:
            return False, f"Keyring error: {e}"

    # ==================== DIAGNOSTICS ====================

    def get_storage_info(self) -> Dict[str, Any]:
        """Get storage information."""
        return {
            "storage_dir": STORAGE_DIR,
            "storage_file": STORAGE_FILE,
            "key_count": len(self._storage),
            "keyring_available": self._keyring_available,
        }
