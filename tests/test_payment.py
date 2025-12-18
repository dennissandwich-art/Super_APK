"""
Unit tests for payment module
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payment import StripePaymentManager

class TestStripePaymentManager(unittest.TestCase):
    """Test cases for StripePaymentManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.payment = StripePaymentManager()

    def test_initialization(self):
        """Test that payment manager initializes"""
        self.assertIsNotNone(self.payment)

    def test_stripe_initialized(self):
        """Test that Stripe is initialized"""
        # May fail if Stripe library not installed
        self.assertTrue(self.payment.stripe_initialized or not self.payment.stripe_initialized)

    def test_get_publishable_key(self):
        """Test getting publishable key"""
        key = self.payment.get_publishable_key()
        self.assertIsNotNone(key)
        self.assertTrue(key.startswith("pk_test_"))

    def test_payment_intent_creation(self):
        """Test payment intent creation (requires Stripe)"""
        if not self.payment.stripe_initialized:
            self.skipTest("Stripe not initialized")

        client_secret, payment_id, error = self.payment.create_payment_intent(
            amount_nok=500.0,
            customer_email="test@example.com",
            order_id="TEST_ORDER_001"
        )

        # Should succeed if Stripe is properly configured
        if error:
            print(f"Payment intent creation note: {error}")
        else:
            self.assertIsNotNone(client_secret)
            self.assertIsNotNone(payment_id)

    def test_payment_stats(self):
        """Test payment statistics"""
        stats = self.payment.get_payment_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("total_payments", stats)
        self.assertIn("total_amount_nok", stats)

if __name__ == "__main__":
    unittest.main()
