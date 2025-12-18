# ai_core.py
# Secure credential storage with encryption

import os
import json
import datetime
from kivy.utils import platform
from cryptography.fernet import Fernet

# =========================
# INTERNAL STORAGE (ANDROID SAFE)
# =========================

if platform == "android":
    from android.storage import app_storage_path
    BASE_DIR = app_storage_path()
else:
    BASE_DIR = os.getcwd()

AI_CONSOLE_DIR = os.path.join(BASE_DIR, "AI_CONSOLES")
os.makedirs(AI_CONSOLE_DIR, exist_ok=True)

# =========================
# AI CONSOLE LOGGER
# =========================

def AI_CONSOLE(scope: str, message: str):
    ts = datetime.datetime.utcnow().isoformat()
    logfile = os.path.join(AI_CONSOLE_DIR, f"{scope}.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")

# =========================
# ENCRYPTION ENGINE
# =========================

KEY_FILE = os.path.join(AI_CONSOLE_DIR, ".master.key")

def _load_master_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    with open(KEY_FILE, "rb") as f:
        return f.read()

FERNET = Fernet(_load_master_key())

def encrypt(raw: str) -> bytes:
    return FERNET.encrypt(raw.encode("utf-8"))

def decrypt(enc: bytes) -> str:
    return FERNET.decrypt(enc).decode("utf-8")

# =========================
# ENCRYPTED API DEFINITIONS
# ALL KEYS LOADED FROM ENVIRONMENT VARIABLES OR SECURE CONFIG
# =========================

def _load_api_key_from_env(key_name):
    """Load API key from environment variable"""
    env_map = {
        'admin_openai': 'ADMIN_OPENAI_KEY',
        'user_openai': 'USER_OPENAI_KEY',
        'groq': 'GROQ_KEY',
        'admin_mistral': 'ADMIN_MISTRAL_KEY',
        'user_mistral': 'USER_MISTRAL_KEY',
        'stripe_publishable': 'STRIPE_PUBLISHABLE_KEY',
        'stripe_secret': 'STRIPE_SECRET_KEY'
    }

    env_var = env_map.get(key_name)
    if env_var:
        return os.getenv(env_var)
    return None

# Helper function to get API keys safely
def get_api_key(key_name):
    """
    Safely retrieve API keys from environment or secure config

    SETUP INSTRUCTIONS:
    Set these environment variables before running the app:

    export ADMIN_OPENAI_KEY="your-key-here"
    export USER_OPENAI_KEY="your-key-here"
    export GROQ_KEY="your-key-here"
    export ADMIN_MISTRAL_KEY="your-key-here"
    export USER_MISTRAL_KEY="your-key-here"
    export STRIPE_PUBLISHABLE_KEY="pk_test_..."
    export STRIPE_SECRET_KEY="sk_test_..."

    Or create a .env file (add to .gitignore!):
    STRIPE_PUBLISHABLE_KEY=pk_test_51Sfh1RI583has4xw...
    STRIPE_SECRET_KEY=sk_test_51Sfh1RI583has4xw...
    """
    try:
        # Try to load from environment
        key_value = _load_api_key_from_env(key_name)

        if key_value:
            AI_CONSOLE("security", f"Key {key_name} loaded from environment")
            return key_value

        # Try to load from secure config file (if exists)
        config_file = os.path.join(AI_CONSOLE_DIR, ".api_keys.enc")
        if os.path.exists(config_file):
            try:
                with open(config_file, "rb") as f:
                    encrypted_data = f.read()
                    decrypted_json = decrypt(encrypted_data)
                    keys = json.loads(decrypted_json)
                    if key_name in keys:
                        AI_CONSOLE("security", f"Key {key_name} loaded from secure config")
                        return keys[key_name]
            except Exception as e:
                AI_CONSOLE("security", f"Failed to load from config: {e}")

        AI_CONSOLE("security", f"Key {key_name} not found - please configure", "WARNING")
        return None

    except Exception as e:
        AI_CONSOLE("security", f"Failed to retrieve key {key_name}: {e}", "ERROR")
        return None

# Function to save keys to encrypted config (for setup)
def save_api_keys(keys_dict):
    """
    Save API keys to encrypted config file

    Usage:
    from modules.ai_core import save_api_keys
    save_api_keys({
        'stripe_publishable': 'pk_test_...',
        'stripe_secret': 'sk_test_...',
        # ... other keys
    })
    """
    try:
        config_file = os.path.join(AI_CONSOLE_DIR, ".api_keys.enc")
        json_data = json.dumps(keys_dict)
        encrypted_data = encrypt(json_data)

        with open(config_file, "wb") as f:
            f.write(encrypted_data)

        # Set restrictive permissions
        os.chmod(config_file, 0o600)

        AI_CONSOLE("security", f"Saved {len(keys_dict)} API keys to encrypted config")
        return True
    except Exception as e:
        AI_CONSOLE("security", f"Failed to save API keys: {e}", "ERROR")
        return False

# Alias function for backward compatibility
def ai_log(scope: str, message: str):
    """Alias for AI_CONSOLE"""
    AI_CONSOLE(scope, message)

def ai_exception(scope: str, exception: Exception):
    """Log exception with traceback"""
    import traceback
    tb = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    AI_CONSOLE(scope, f"EXCEPTION: {str(exception)}\n{tb}")

# =========================
# SELF-HEAL ENGINE (MANDATORY)
# =========================

def self_healf(context="runtime"):
    """
    Live validation of app state.
    Logs filesystem, module presence, permissions, and AI readiness.
    """
    AI_CONSOLE("self_healf", f"START context={context}")

    try:
        AI_CONSOLE("self_healf", f"Platform={platform}")
        AI_CONSOLE("self_healf", f"BaseDir={BASE_DIR}")
        AI_CONSOLE("self_healf", f"ConsoleDirExists={os.path.exists(AI_CONSOLE_DIR)}")

        # API sanity - test key retrieval system
        test_keys = ['stripe_publishable', 'stripe_secret']
        keys_found = 0

        for key_name in test_keys:
            key_val = get_api_key(key_name)
            if key_val:
                AI_CONSOLE("self_healf", f"Key {key_name}: OK ({len(key_val)} chars)")
                keys_found += 1
            else:
                AI_CONSOLE("self_healf", f"Key {key_name}: NOT CONFIGURED")

        if keys_found > 0:
            AI_CONSOLE("self_healf", f"API_KEY_SYSTEM_OK ({keys_found} keys configured)")
        else:
            AI_CONSOLE("self_healf", "API_KEY_SYSTEM_WARNING (no keys configured yet)")

    except Exception as e:
        AI_CONSOLE("self_healf", f"FAIL {repr(e)}")
        raise

    AI_CONSOLE("self_healf", "END OK")
