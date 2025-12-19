# backend/store/user_store.py
# ROLE: User persistence (MINIMAL, ONE TABLE)

"""
PERSISTENCE CONTRACT:
Table: users
- tg_user_id: integer PRIMARY KEY
- username: text (nullable)
- first_seen: timestamp
- last_seen: timestamp

No other tables in early phase.
"""

import sqlite3
import time
import os
from typing import Optional


class UserStore:
    def __init__(self, db_path: str = "./data/users.db"):
        self._db_path = db_path
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self):
        """Ensure data directory exists."""
        directory = os.path.dirname(self._db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    tg_user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_seen INTEGER NOT NULL,
                    last_seen INTEGER NOT NULL
                )
            """)
            conn.commit()

    def upsert_user(self, tg_user_id: int, username: Optional[str] = None) -> bool:
        """
        Insert or update user.
        Returns True on success, False on failure.
        """
        try:
            current_time = int(time.time())
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("""
                    INSERT INTO users (tg_user_id, username, first_seen, last_seen)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(tg_user_id) DO UPDATE SET
                        username = excluded.username,
                        last_seen = excluded.last_seen
                """, (tg_user_id, username, current_time, current_time))
                conn.commit()
            return True
        except Exception:
            return False

    def get_user(self, tg_user_id: int) -> Optional[dict]:
        """Get user by tg_user_id. Returns None if not found."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute(
                    "SELECT tg_user_id, username, first_seen, last_seen FROM users WHERE tg_user_id = ?",
                    (tg_user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return {
                        "tg_user_id": row[0],
                        "username": row[1],
                        "first_seen": row[2],
                        "last_seen": row[3]
                    }
            return None
        except Exception:
            return None
