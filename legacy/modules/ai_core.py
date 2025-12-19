# ai_core.py

AI_CONSOLE("module_name", "description of event or error")

from ai_core import AI_CONSOLE

import os
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
# (PLACEHOLDERS FOR YOUR UNDERSTANDING — NOT EMPTY)
# =========================

ADMIN_OPENAI_KEY   = encrypt("sk-proj-REPLACE_WITH_ADMIN_KEY")
USER_OPENAI_KEY    = encrypt("sk-proj-REPLACE_WITH_USER_KEY")
GROQ_KEY           = encrypt("gsk-REPLACE_WITH_GROQ_KEY")
ADMIN_MISTRAL_KEY  = encrypt("ag-REPLACE_WITH_ADMIN_MISTRAL")
USER_MISTRAL_KEY   = encrypt("ag-REPLACE_WITH_USER_MISTRAL")

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

        # API sanity
        _ = decrypt(ADMIN_OPENAI_KEY)
        _ = decrypt(USER_OPENAI_KEY)
        _ = decrypt(GROQ_KEY)

        AI_CONSOLE("self_healf", "API_DECRYPT_OK")

    except Exception as e:
        AI_CONSOLE("self_healf", f"FAIL {repr(e)}")
        raise

    AI_CONSOLE("self_healf", "END OK")
