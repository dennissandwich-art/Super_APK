# payments/key_store.py
# BRANCH: claude-setup-stripe-align-code
# ROLE: Secure key reference layer (NO KEYS STORED)

"""
This module represents a future encrypted keystore.
Currently, it only holds placeholders and references.
"""

# PLACEHOLDER STORAGE
# In production this could be replaced with:
# - Android Keystore
# - Encrypted file
# - Remote secrets service

_ENCRYPTED_KEYS = {
    "STRIPE_API_KEY": None,
}


def set_key(name: str, value: str) -> None:
    if name not in _ENCRYPTED_KEYS:
        raise KeyError("Unknown key reference")
    _ENCRYPTED_KEYS[name] = value


def get_key(name: str):
    return _ENCRYPTED_KEYS.get(name)
