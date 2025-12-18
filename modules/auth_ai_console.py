# modules/auth_ai_console.py

from kivy.utils import platform
import os, datetime
from cryptography.fernet import Fernet

# 1️⃣ Internal Storage Setup
if platform == "android":
    from android.storage import app_storage_path
    STORAGE_DIR = os.path.join(app_storage_path(), "AI_consoles")
else:
    STORAGE_DIR = "./AI_consoles"

os.makedirs(STORAGE_DIR, exist_ok=True)

# 2️⃣ AI Console Logger
def AI_CONSOLE(scope: str, msg: str):
    """
    Logs all AI activity for debugging and auditing.
    """
    ts = datetime.datetime.utcnow().isoformat()
    log_file = os.path.join(STORAGE_DIR, f"{scope}.log")
    with open(log_file, "a") as f:
        f.write(f"[{ts}] {msg}\n")

# 3️⃣ Encrypted API Keys
KEY_FILE = os.path.join(STORAGE_DIR, ".master_key")

def get_master_key() -> bytes:
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    return open(KEY_FILE, "rb").read()

_FERNET = Fernet(get_master_key())

def encrypt(value: str) -> bytes:
    return _FERNET.encrypt(value.encode())

def decrypt(value: bytes) -> str:
    return _FERNET.decrypt(value).decode()

# 4️⃣ Encrypted API placeholders
ADMIN_OPEN_AI_API = encrypt("sk-proj-ADMIN_YOUR_KEY_HERE")
USER_OPEN_AI_API = encrypt("sk-proj-USER_YOUR_KEY_HERE")
GROQ_AI_API = encrypt("gsk-USER_YOUR_KEY_HERE")
ADMIN_MISTRAL_API = encrypt("ag-ADMIN_YOUR_KEY_HERE")
USER_MISTRAL_API = encrypt("ag-USER_YOUR_KEY_HERE")

# 5️⃣ Usage Example
def init_api():
    AI_CONSOLE("auth", "Initializing API keys for runtime use")
    admin_key = decrypt(ADMIN_OPEN_AI_API)
    AI_CONSOLE("auth", f"Admin API key ready: {admin_key[:4]}**** (hidden)")
    return admin_key
