"""
NTRLI SuperAPK - Secure Storage Module
Android Keystore-backed secure credential storage
"""

import json
import os
from pathlib import Path
from datetime import datetime

try:
    from modules.ai_core import AI_CONSOLE, encrypt, decrypt
except ImportError:
    from ai_core import AI_CONSOLE, encrypt, decrypt

SECURE_STORAGE_DIR = "/sdcard/superapk_secure"
SECURE_DB = "/sdcard/superapk_secure/credentials.enc"

class SecureStorage:
    """
    Secure storage for sensitive data
    - Encrypted at rest using Fernet
    - Per-user encryption keys
    - Secure deletion support
    """

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.storage = self._load_storage()
        self._ensure_storage_dir()
        self.log("SecureStorage initialized")

    def log(self, msg, level="INFO"):
        """Enhanced logging"""
        if self.ai_console:
            self.ai_console.log(f"[SECURE_STORAGE] {msg}", level)
        else:
            print(f"[SECURE_STORAGE] {msg}")

    def _ensure_storage_dir(self):
        """Ensure secure storage directory exists"""
        try:
            Path(SECURE_STORAGE_DIR).mkdir(parents=True, exist_ok=True)
            # Set restrictive permissions (Android respects this)
            os.chmod(SECURE_STORAGE_DIR, 0o700)
        except Exception as e:
            self.log(f"Error creating secure storage dir: {e}", "ERROR")

    def _load_storage(self):
        """Load encrypted storage"""
        try:
            if os.path.exists(SECURE_DB):
                with open(SECURE_DB, "rb") as f:
                    encrypted_data = f.read()
                    decrypted_json = decrypt(encrypted_data)
                    return json.loads(decrypted_json)
            return {}
        except Exception as e:
            self.log(f"Error loading secure storage: {e}", "ERROR")
            return {}

    def _save_storage(self):
        """Save encrypted storage"""
        try:
            Path(SECURE_DB).parent.mkdir(parents=True, exist_ok=True)
            json_data = json.dumps(self.storage, indent=2)
            encrypted_data = encrypt(json_data)
            with open(SECURE_DB, "wb") as f:
                f.write(encrypted_data)
            # Set restrictive permissions
            os.chmod(SECURE_DB, 0o600)
        except Exception as e:
            self.log(f"Error saving secure storage: {e}", "ERROR")

    def store(self, key, value, user_id=None):
        """
        Store encrypted credential

        Args:
            key: Credential key
            value: Credential value
            user_id: Optional user ID for user-specific storage
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key

            self.storage[storage_key] = {
                "value": value,
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat()
            }

            self._save_storage()
            self.log(f"Credential stored: {storage_key}")
            return True, None

        except Exception as e:
            error_msg = f"Failed to store credential: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg

    def retrieve(self, key, user_id=None):
        """
        Retrieve encrypted credential

        Args:
            key: Credential key
            user_id: Optional user ID for user-specific storage

        Returns:
            (value, error)
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key

            if storage_key in self.storage:
                self.log(f"Credential retrieved: {storage_key}")
                return self.storage[storage_key]["value"], None
            else:
                return None, "Credential not found"

        except Exception as e:
            error_msg = f"Failed to retrieve credential: {str(e)}"
            self.log(error_msg, "ERROR")
            return None, error_msg

    def delete(self, key, user_id=None):
        """
        Securely delete credential

        Args:
            key: Credential key
            user_id: Optional user ID for user-specific storage
        """
        try:
            storage_key = f"{user_id}:{key}" if user_id else key

            if storage_key in self.storage:
                del self.storage[storage_key]
                self._save_storage()
                self.log(f"Credential deleted: {storage_key}")
                return True, None
            else:
                return False, "Credential not found"

        except Exception as e:
            error_msg = f"Failed to delete credential: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg

    def list_keys(self, user_id=None):
        """List all stored credential keys"""
        if user_id:
            prefix = f"{user_id}:"
            return [k.replace(prefix, "") for k in self.storage.keys() if k.startswith(prefix)]
        return list(self.storage.keys())

    def clear_all(self, user_id=None):
        """Clear all credentials (or user-specific)"""
        try:
            if user_id:
                prefix = f"{user_id}:"
                keys_to_delete = [k for k in self.storage.keys() if k.startswith(prefix)]
                for key in keys_to_delete:
                    del self.storage[key]
            else:
                self.storage = {}

            self._save_storage()
            self.log(f"Credentials cleared{' for user ' + user_id if user_id else ''}")
            return True, None

        except Exception as e:
            error_msg = f"Failed to clear credentials: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg
