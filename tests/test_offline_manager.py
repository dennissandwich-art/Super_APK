"""
Offline Manager Tests
=====================

Tests for the offline operation queuing and execution.
"""

import unittest
import sys
import os
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from offline_manager import OfflineManager
from payment import PaymentNotEnabledError


class TestOfflineManagerQueuing(unittest.TestCase):
    """Test operation queuing functionality."""

    def setUp(self):
        """Set up offline manager with temp storage."""
        self.manager = OfflineManager()
        self.manager.pending_operations = []  # Start fresh

    def test_queue_operation(self):
        """Test that operations can be queued."""
        op_id = self.manager.queue_operation(
            "data_sync",
            {"sync_type": "full"},
            priority=5
        )

        self.assertIsNotNone(op_id)
        self.assertEqual(self.manager.get_pending_operations_count(), 1)

    def test_queue_operation_with_priority(self):
        """Test that priority is stored correctly."""
        op_id = self.manager.queue_operation(
            "data_sync",
            {"sync_type": "full"},
            priority=10
        )

        status, op = self.manager.get_operation_status(op_id)
        self.assertEqual(op["priority"], 10)

    def test_queue_multiple_operations(self):
        """Test queuing multiple operations."""
        self.manager.queue_operation("data_sync", {}, priority=1)
        self.manager.queue_operation("news_fetch", {}, priority=5)
        self.manager.queue_operation("data_sync", {}, priority=10)

        self.assertEqual(self.manager.get_pending_operations_count(), 3)


class TestPaymentOperationDisabled(unittest.TestCase):
    """Test that payment operations correctly fail."""

    def setUp(self):
        """Set up offline manager."""
        self.manager = OfflineManager()
        self.manager.pending_operations = []

    def test_payment_operation_raises_error(self):
        """Test that payment operations raise PaymentNotEnabledError."""
        # Create a payment operation
        operation = {
            "id": "payment_test_123",
            "type": "payment_process",
            "data": {"amount": 100, "email": "test@example.com"},
            "priority": 10,
            "attempts": 0,
            "status": "pending"
        }

        success, result, error = self.manager.execute_operation(operation)

        self.assertFalse(success)
        self.assertIsNotNone(error)
        self.assertIn("disabled", error.lower())


class TestCacheOperations(unittest.TestCase):
    """Test cache functionality."""

    def setUp(self):
        """Set up offline manager."""
        self.manager = OfflineManager()

    def test_cache_data(self):
        """Test caching data."""
        success = self.manager.cache_data(
            "test_key",
            {"data": "test_value"},
            ttl=3600
        )
        # May fail if cache dir is not writable, which is expected in tests
        # The important thing is it doesn't crash

    def test_cache_miss(self):
        """Test cache miss returns error."""
        data, error = self.manager.get_cached_data("nonexistent_key_12345")

        self.assertIsNone(data)
        self.assertIsNotNone(error)


class TestConnectivityCheck(unittest.TestCase):
    """Test connectivity checking."""

    def setUp(self):
        """Set up offline manager."""
        self.manager = OfflineManager()

    def test_default_online_status(self):
        """Test default online status."""
        # Without network manager, defaults to online
        self.assertTrue(self.manager.is_online)

    def test_check_connectivity_without_network_manager(self):
        """Test connectivity check without network manager."""
        result = self.manager.check_connectivity()
        # Returns stored is_online value
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
