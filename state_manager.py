"""
NTRLI SuperAPK - State Management Module
Redux-style centralized state management
"""

import json
import copy
from datetime import datetime

try:
    from modules.ai_core import AI_CONSOLE
except ImportError:
    from ai_core import AI_CONSOLE

class AppState:
    """
    Centralized application state management
    - Single source of truth
    - Immutable state updates
    - Subscriber pattern for reactivity
    - Time-travel debugging support
    """

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.state = self._get_initial_state()
        self.subscribers = []
        self.history = []  # For time-travel debugging
        self.max_history = 50
        self.log("StateManager initialized")

    def log(self, msg, level="INFO"):
        """Enhanced logging"""
        if self.ai_console:
            self.ai_console.log(f"[STATE] {msg}", level)
        else:
            print(f"[STATE] {msg}")

    def _get_initial_state(self):
        """Get initial application state"""
        return {
            "app": {
                "version": "1.0.11",
                "initialized": False,
                "theme": "dark",
                "language": "en"
            },
            "user": {
                "logged_in": False,
                "username": None,
                "role": None,
                "session_token": None
            },
            "cart": {
                "items": [],
                "total": 0.0,
                "item_count": 0
            },
            "news": {
                "articles": [],
                "last_fetched": None,
                "selected_category": None
            },
            "network": {
                "status": "online",
                "last_check": None,
                "tor_enabled": False,
                "vpn_enabled": False
            },
            "payment": {
                "processing": False,
                "last_transaction": None
            },
            "offline": {
                "pending_operations": 0,
                "last_sync": None
            },
            "ai": {
                "active_model": "claude",
                "conversation_active": False
            },
            "ui": {
                "current_screen": "home",
                "loading": False,
                "error_message": None
            }
        }

    def get_state(self, path=None):
        """
        Get current state (or nested path)

        Args:
            path: Optional dot-notation path (e.g., "user.username")

        Returns:
            State value
        """
        if path is None:
            return copy.deepcopy(self.state)

        # Navigate nested path
        keys = path.split(".")
        value = self.state
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None

        return copy.deepcopy(value)

    def dispatch(self, action):
        """
        Dispatch an action to update state

        Args:
            action: Dict with 'type' and optional 'payload'
                   e.g., {"type": "USER_LOGIN", "payload": {"username": "test"}}

        Returns:
            new_state
        """
        try:
            action_type = action.get("type")
            payload = action.get("payload", {})

            self.log(f"Dispatching action: {action_type}")

            # Store previous state in history
            self._add_to_history(action)

            # Compute new state based on action
            new_state = self.reducer(self.state, action)

            # Update state
            self.state = new_state

            # Notify subscribers
            self._notify_subscribers(action, new_state)

            return new_state

        except Exception as e:
            self.log(f"Dispatch error: {e}", "ERROR")
            return self.state

    def reducer(self, state, action):
        """
        Redux-style reducer - pure function that updates state

        Args:
            state: Current state
            action: Action to process

        Returns:
            new_state
        """
        new_state = copy.deepcopy(state)
        action_type = action.get("type")
        payload = action.get("payload", {})

        # User actions
        if action_type == "USER_LOGIN":
            new_state["user"]["logged_in"] = True
            new_state["user"]["username"] = payload.get("username")
            new_state["user"]["role"] = payload.get("role")
            new_state["user"]["session_token"] = payload.get("session_token")

        elif action_type == "USER_LOGOUT":
            new_state["user"] = self._get_initial_state()["user"]
            new_state["cart"] = self._get_initial_state()["cart"]

        # Cart actions
        elif action_type == "CART_ADD_ITEM":
            new_state["cart"]["items"].append(payload)
            self._recalculate_cart(new_state["cart"])

        elif action_type == "CART_REMOVE_ITEM":
            product_id = payload.get("product_id")
            new_state["cart"]["items"] = [
                item for item in new_state["cart"]["items"]
                if item.get("product_id") != product_id
            ]
            self._recalculate_cart(new_state["cart"])

        elif action_type == "CART_CLEAR":
            new_state["cart"] = self._get_initial_state()["cart"]

        # News actions
        elif action_type == "NEWS_FETCHED":
            new_state["news"]["articles"] = payload.get("articles", [])
            new_state["news"]["last_fetched"] = datetime.now().isoformat()

        elif action_type == "NEWS_SELECT_CATEGORY":
            new_state["news"]["selected_category"] = payload.get("category")

        # Network actions
        elif action_type == "NETWORK_STATUS_CHANGE":
            new_state["network"]["status"] = payload.get("status")
            new_state["network"]["last_check"] = datetime.now().isoformat()

        # Payment actions
        elif action_type == "PAYMENT_START":
            new_state["payment"]["processing"] = True

        elif action_type == "PAYMENT_COMPLETE":
            new_state["payment"]["processing"] = False
            new_state["payment"]["last_transaction"] = payload
            new_state["cart"] = self._get_initial_state()["cart"]

        elif action_type == "PAYMENT_FAILED":
            new_state["payment"]["processing"] = False

        # UI actions
        elif action_type == "UI_NAVIGATE":
            new_state["ui"]["current_screen"] = payload.get("screen")

        elif action_type == "UI_LOADING":
            new_state["ui"]["loading"] = payload.get("loading", True)

        elif action_type == "UI_ERROR":
            new_state["ui"]["error_message"] = payload.get("message")

        elif action_type == "UI_CLEAR_ERROR":
            new_state["ui"]["error_message"] = None

        # App actions
        elif action_type == "APP_INITIALIZED":
            new_state["app"]["initialized"] = True

        elif action_type == "APP_SET_LANGUAGE":
            new_state["app"]["language"] = payload.get("language")

        elif action_type == "APP_SET_THEME":
            new_state["app"]["theme"] = payload.get("theme")

        return new_state

    def _recalculate_cart(self, cart):
        """Recalculate cart totals"""
        cart["item_count"] = len(cart["items"])
        cart["total"] = sum(
            item.get("price", 0) * item.get("quantity", 1)
            for item in cart["items"]
        )

    def subscribe(self, callback):
        """
        Subscribe to state changes

        Args:
            callback: Function to call when state changes
                     callback(action, new_state)

        Returns:
            unsubscribe function
        """
        self.subscribers.append(callback)
        self.log(f"Subscriber added (total: {len(self.subscribers)})")

        # Return unsubscribe function
        def unsubscribe():
            if callback in self.subscribers:
                self.subscribers.remove(callback)
                self.log(f"Subscriber removed (total: {len(self.subscribers)})")

        return unsubscribe

    def _notify_subscribers(self, action, new_state):
        """Notify all subscribers of state change"""
        for callback in self.subscribers:
            try:
                callback(action, new_state)
            except Exception as e:
                self.log(f"Subscriber callback error: {e}", "ERROR")

    def _add_to_history(self, action):
        """Add state snapshot to history"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "state": copy.deepcopy(self.state)
        }
        self.history.append(snapshot)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self, limit=10):
        """Get state history (for debugging)"""
        return self.history[-limit:]

    def time_travel(self, index):
        """
        Time-travel debugging: restore state from history

        Args:
            index: History index (negative for recent)

        Returns:
            success
        """
        try:
            if abs(index) > len(self.history):
                return False

            snapshot = self.history[index]
            self.state = copy.deepcopy(snapshot["state"])
            self.log(f"Time-traveled to state at {snapshot['timestamp']}")

            # Notify subscribers
            self._notify_subscribers(
                {"type": "TIME_TRAVEL", "payload": {"index": index}},
                self.state
            )

            return True

        except Exception as e:
            self.log(f"Time-travel error: {e}", "ERROR")
            return False

    def export_state(self):
        """Export state as JSON"""
        return json.dumps(self.state, indent=2)

    def import_state(self, json_state):
        """Import state from JSON"""
        try:
            self.state = json.loads(json_state)
            self.log("State imported")
            self._notify_subscribers(
                {"type": "STATE_IMPORTED", "payload": {}},
                self.state
            )
            return True
        except Exception as e:
            self.log(f"State import error: {e}", "ERROR")
            return False
