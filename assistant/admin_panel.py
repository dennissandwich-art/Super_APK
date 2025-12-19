# assistant/admin_panel.py
# BRANCH: main
# ROLE: Admin panel powered by AI Assistant

"""
ADMIN PANEL:
- Deep AI assistant integration
- System monitoring
- User management
- Configuration control
- Live checkups
- Research capability

The admin panel IS the AI assistant interface.
"""

from typing import Dict, List, Optional, Callable
from assistant.core import AIAssistant


class AdminPanel:
    """
    Admin panel powered by AI Assistant.
    Single interface for all administrative functions.
    """

    def __init__(self, config: Dict = None):
        self._config = config or {}
        self._assistant = AIAssistant(config)
        self._admin_token: Optional[str] = None
        self._authenticated = False

        # Panel state
        self._current_view = "dashboard"
        self._notifications: List[Dict] = []

    # ==================
    # AUTHENTICATION
    # ==================

    def authenticate(self, token: str) -> Dict:
        """Authenticate admin session."""
        # In production: verify against session manager
        if token and len(token) > 0:
            self._admin_token = token
            self._authenticated = True
            return {"status": "ok", "authenticated": True}
        return {"status": "error", "reason": "Invalid token"}

    def logout(self):
        """Logout admin session."""
        self._admin_token = None
        self._authenticated = False

    def is_authenticated(self) -> bool:
        """Check if admin is authenticated."""
        return self._authenticated

    # ==================
    # DASHBOARD
    # ==================

    def get_dashboard(self) -> Dict:
        """Get dashboard overview."""
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return {
            "status": "ok",
            "system_status": self._get_system_status(),
            "recent_activity": self._get_recent_activity(),
            "notifications": self._notifications[-10:],
            "quick_stats": self._get_quick_stats()
        }

    def _get_system_status(self) -> Dict:
        """Get system status for dashboard."""
        checkup = self._assistant.checkup()
        return {
            "overall": checkup.get("status", "unknown"),
            "checks": checkup.get("checks", [])
        }

    def _get_recent_activity(self) -> List[Dict]:
        """Get recent activity."""
        # Placeholder - would connect to activity log
        return []

    def _get_quick_stats(self) -> Dict:
        """Get quick stats for dashboard."""
        return {
            "assistant_ready": True,
            "capabilities": len(self._assistant._capabilities.list_all())
        }

    # ==================
    # AI ASSISTANT INTERFACE
    # ==================

    def ask(self, question: str) -> Dict:
        """
        Ask the AI assistant.
        Primary interface for admin panel.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.admin_query(question, self._admin_token)

    def execute(self, action: str, params: Dict = None) -> Dict:
        """
        Execute an action through the assistant.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.execute_admin_action(
            action,
            params or {},
            self._admin_token
        )

    def research(self, topic: str) -> Dict:
        """
        Perform research through the assistant.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.research(topic)

    def validate(self, data, schema: str = None) -> Dict:
        """
        Validate data through the assistant.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.validate(data, schema)

    def consolidate(self, sources: List[Dict]) -> Dict:
        """
        Consolidate data through the assistant.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.consolidate(sources)

    def checkup(self) -> Dict:
        """
        Run system checkup through the assistant.
        """
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.checkup()

    # ==================
    # SYSTEM MANAGEMENT
    # ==================

    def get_system_state(self) -> Dict:
        """Get complete system state."""
        if not self._authenticated:
            return {"status": "error", "reason": "Not authenticated"}

        return self._assistant.get_system_state(self._admin_token)

    def get_capabilities(self) -> List[Dict]:
        """List all assistant capabilities."""
        if not self._authenticated:
            return []

        return self._assistant._capabilities.list_all()

    # ==================
    # NOTIFICATIONS
    # ==================

    def add_notification(self, title: str, message: str, level: str = "info"):
        """Add notification to panel."""
        import time
        self._notifications.append({
            "timestamp": int(time.time()),
            "title": title,
            "message": message,
            "level": level,
            "read": False
        })

        # Keep bounded
        if len(self._notifications) > 100:
            self._notifications = self._notifications[-50:]

    def get_notifications(self, unread_only: bool = False) -> List[Dict]:
        """Get notifications."""
        if unread_only:
            return [n for n in self._notifications if not n["read"]]
        return self._notifications

    def mark_read(self, timestamp: int):
        """Mark notification as read."""
        for n in self._notifications:
            if n["timestamp"] == timestamp:
                n["read"] = True
                break

    # ==================
    # NAVIGATION
    # ==================

    def navigate(self, view: str) -> Dict:
        """Navigate to a view."""
        valid_views = ["dashboard", "users", "config", "logs", "research", "assistant"]
        if view not in valid_views:
            return {"status": "error", "reason": f"Invalid view: {view}"}

        self._current_view = view
        return {"status": "ok", "view": view}

    def get_current_view(self) -> str:
        """Get current view."""
        return self._current_view
