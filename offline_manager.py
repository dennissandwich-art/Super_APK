"""
NTRLI SuperAPK - Offline Manager Module
Offline-first architecture with operation queuing and sync
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

try:
    from modules.ai_core import AI_CONSOLE
except ImportError:
    from ai_core import AI_CONSOLE

PENDING_OPS_DB = "/sdcard/superapk_pending_ops.json"
OFFLINE_CACHE_DIR = "/sdcard/superapk_cache"

class OfflineManager:
    """
    Manages offline operations and syncing
    - Queues operations when offline
    - Auto-syncs when connection restored
    - Caches data for offline access
    """

    def __init__(self, ai_console=None, network_manager=None):
        self.ai_console = ai_console
        self.network_manager = network_manager
        self.pending_operations = self._load_pending_operations()
        self.is_online = True
        self._ensure_cache_dir()
        self.log("OfflineManager initialized")

    def log(self, msg, level="INFO"):
        """Enhanced logging"""
        if self.ai_console:
            self.ai_console.log(f"[OFFLINE] {msg}", level)
        else:
            print(f"[OFFLINE] {msg}")

    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        try:
            Path(OFFLINE_CACHE_DIR).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log(f"Error creating cache dir: {e}", "ERROR")

    def _load_pending_operations(self):
        """Load pending operations queue"""
        try:
            if os.path.exists(PENDING_OPS_DB):
                with open(PENDING_OPS_DB, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.log(f"Error loading pending operations: {e}", "ERROR")
            return []

    def _save_pending_operations(self):
        """Save pending operations queue"""
        try:
            Path(PENDING_OPS_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(PENDING_OPS_DB, "w") as f:
                json.dump(self.pending_operations, f, indent=2)
        except Exception as e:
            self.log(f"Error saving pending operations: {e}", "ERROR")

    def check_connectivity(self):
        """Check network connectivity"""
        if self.network_manager:
            connected, _ = self.network_manager.check_connectivity()
            self.is_online = connected
            return connected
        return self.is_online

    def queue_operation(self, op_type, data, priority=5):
        """
        Queue an operation for later execution

        Args:
            op_type: Operation type (e.g., 'payment', 'order', 'sync')
            data: Operation data
            priority: Priority (1-10, 10 is highest)

        Returns:
            operation_id
        """
        try:
            operation = {
                "id": f"{op_type}_{int(time.time() * 1000)}",
                "type": op_type,
                "data": data,
                "priority": priority,
                "queued_at": datetime.now().isoformat(),
                "attempts": 0,
                "last_attempt": None,
                "status": "pending"
            }

            self.pending_operations.append(operation)
            self._save_pending_operations()

            self.log(f"Operation queued: {operation['id']} (type: {op_type}, priority: {priority})")
            return operation["id"]

        except Exception as e:
            self.log(f"Failed to queue operation: {e}", "ERROR")
            return None

    def execute_operation(self, operation):
        """
        Execute a queued operation

        Args:
            operation: The operation dict

        Returns:
            (success, result, error)
        """
        try:
            operation["attempts"] += 1
            operation["last_attempt"] = datetime.now().isoformat()

            op_type = operation["type"]
            data = operation["data"]

            self.log(f"Executing operation: {operation['id']} (attempt {operation['attempts']})")

            # Route to appropriate handler based on operation type
            if op_type == "order_create":
                result = self._execute_order_create(data)
            elif op_type == "payment_process":
                result = self._execute_payment_process(data)
            elif op_type == "data_sync":
                result = self._execute_data_sync(data)
            elif op_type == "news_fetch":
                result = self._execute_news_fetch(data)
            else:
                return False, None, f"Unknown operation type: {op_type}"

            operation["status"] = "completed"
            self.log(f"Operation completed: {operation['id']}")
            return True, result, None

        except Exception as e:
            error_msg = f"Operation failed: {str(e)}"
            self.log(error_msg, "ERROR")
            operation["status"] = "failed"
            operation["error"] = error_msg
            return False, None, error_msg

    def _execute_order_create(self, data):
        """Execute order creation"""
        # Import here to avoid circular imports
        from ecommerce import EcommerceManager
        ecom = EcommerceManager(self.ai_console)
        success, result = ecom.checkout(data.get("user_info"))
        if not success:
            raise Exception(result)
        return result

    def _execute_payment_process(self, data):
        """
        Execute payment processing.

        NOTE: Payments are currently disabled. This will raise an error.
        Payment operations are queued but cannot be processed until
        the payment module is properly implemented with security requirements.
        """
        from payment import PaymentManager, PaymentNotEnabledError

        # Check if payments are enabled
        payment = PaymentManager()
        if not payment.is_enabled():
            raise PaymentNotEnabledError(
                "Payment processing is disabled. "
                "Operation queued but cannot be executed. "
                "See sandbox/stripe-experiment/ for development."
            )

        # This code won't be reached while payments are disabled
        return {"status": "payment_disabled", "queued": True}

    def _execute_data_sync(self, data):
        """Execute data synchronization"""
        self.log(f"Syncing data: {data.get('sync_type')}")
        # Implement actual sync logic here
        return {"synced": True}

    def _execute_news_fetch(self, data):
        """Execute news fetch"""
        from news import NewsManager
        news = NewsManager(self.ai_console, self.network_manager)
        articles = news.fetch_all_feeds()
        return {"articles_count": len(articles)}

    def sync_pending_operations(self):
        """
        Sync all pending operations when online

        Returns:
            (completed_count, failed_count)
        """
        if not self.check_connectivity():
            self.log("Cannot sync: offline", "WARNING")
            return 0, 0

        # Sort by priority (highest first) and timestamp (oldest first)
        sorted_ops = sorted(
            self.pending_operations,
            key=lambda x: (-x["priority"], x["queued_at"])
        )

        completed = 0
        failed = 0

        for operation in sorted_ops[:]:  # Copy list to allow removal during iteration
            if operation["status"] != "pending":
                continue

            # Skip if too many attempts
            if operation["attempts"] >= 3:
                operation["status"] = "abandoned"
                failed += 1
                self.log(f"Operation abandoned after 3 attempts: {operation['id']}", "WARNING")
                continue

            success, result, error = self.execute_operation(operation)

            if success:
                completed += 1
                # Remove from queue
                self.pending_operations.remove(operation)
            else:
                failed += 1

        self._save_pending_operations()

        self.log(f"Sync completed: {completed} successful, {failed} failed")
        return completed, failed

    def cache_data(self, cache_key, data, ttl=3600):
        """
        Cache data for offline access

        Args:
            cache_key: Unique cache key
            data: Data to cache
            ttl: Time to live in seconds

        Returns:
            success
        """
        try:
            cache_file = os.path.join(OFFLINE_CACHE_DIR, f"{cache_key}.json")

            cache_entry = {
                "data": data,
                "cached_at": datetime.now().isoformat(),
                "expires_at": datetime.now().timestamp() + ttl
            }

            with open(cache_file, "w") as f:
                json.dump(cache_entry, f, indent=2)

            self.log(f"Data cached: {cache_key} (TTL: {ttl}s)")
            return True

        except Exception as e:
            self.log(f"Cache write failed: {e}", "ERROR")
            return False

    def get_cached_data(self, cache_key):
        """
        Retrieve cached data

        Args:
            cache_key: Unique cache key

        Returns:
            (data, error)
        """
        try:
            cache_file = os.path.join(OFFLINE_CACHE_DIR, f"{cache_key}.json")

            if not os.path.exists(cache_file):
                return None, "Cache miss"

            with open(cache_file, "r") as f:
                cache_entry = json.load(f)

            # Check if expired
            if datetime.now().timestamp() > cache_entry["expires_at"]:
                os.remove(cache_file)
                return None, "Cache expired"

            self.log(f"Cache hit: {cache_key}")
            return cache_entry["data"], None

        except Exception as e:
            self.log(f"Cache read failed: {e}", "ERROR")
            return None, str(e)

    def clear_cache(self, cache_key=None):
        """Clear cache (all or specific key)"""
        try:
            if cache_key:
                cache_file = os.path.join(OFFLINE_CACHE_DIR, f"{cache_key}.json")
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    self.log(f"Cache cleared: {cache_key}")
            else:
                # Clear all cache files
                for cache_file in Path(OFFLINE_CACHE_DIR).glob("*.json"):
                    os.remove(cache_file)
                self.log("All cache cleared")

            return True

        except Exception as e:
            self.log(f"Cache clear failed: {e}", "ERROR")
            return False

    def get_pending_operations_count(self):
        """Get count of pending operations"""
        return len([op for op in self.pending_operations if op["status"] == "pending"])

    def get_operation_status(self, operation_id):
        """Get status of a specific operation"""
        for op in self.pending_operations:
            if op["id"] == operation_id:
                return op["status"], op
        return None, None
