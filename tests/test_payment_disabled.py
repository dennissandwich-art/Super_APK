"""
Payment Module Tests
====================

These tests verify that the payment module correctly blocks
all payment operations until security requirements are met.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from payment import PaymentManager, PaymentNotEnabledError, StripePaymentManager


class TestPaymentDisabled(unittest.TestCase):
    """Test that payment operations are properly disabled."""

    def setUp(self):
        """Set up payment manager."""
        self.payment = PaymentManager()

    def test_payment_not_enabled(self):
        """Test that payments are disabled by default."""
        self.assertFalse(self.payment.is_enabled())

    def test_create_payment_intent_raises(self):
        """Test that create_payment_intent raises PaymentNotEnabledError."""
        with self.assertRaises(PaymentNotEnabledError) as context:
            self.payment.create_payment_intent(100, "test@example.com")

        self.assertIn("not enabled", str(context.exception))
        self.assertIn("sandbox/stripe-experiment", str(context.exception))

    def test_confirm_payment_raises(self):
        """Test that confirm_payment raises PaymentNotEnabledError."""
        with self.assertRaises(PaymentNotEnabledError) as context:
            self.payment.confirm_payment("pi_test123")

        self.assertIn("not enabled", str(context.exception))

    def test_process_payment_raises(self):
        """Test that process_payment raises PaymentNotEnabledError."""
        with self.assertRaises(PaymentNotEnabledError) as context:
            self.payment.process_payment({"amount": 100})

        self.assertIn("not enabled", str(context.exception))

    def test_stripe_alias_also_disabled(self):
        """Test that StripePaymentManager alias is also disabled."""
        payment = StripePaymentManager()
        self.assertFalse(payment.is_enabled())


class TestPaymentErrorMessages(unittest.TestCase):
    """Test that error messages are informative."""

    def setUp(self):
        """Set up payment manager."""
        self.payment = PaymentManager()

    def test_error_message_mentions_security(self):
        """Test that error messages mention security requirements."""
        try:
            self.payment.create_payment_intent(100, "test@example.com")
            self.fail("Should have raised PaymentNotEnabledError")
        except PaymentNotEnabledError as e:
            error_str = str(e).lower()
            # Should mention security or compliance
            self.assertTrue(
                "security" in error_str or
                "pci" in error_str or
                "sandbox" in error_str,
                f"Error should mention security requirements: {e}"
            )

    def test_error_message_provides_guidance(self):
        """Test that error messages provide guidance on next steps."""
        try:
            self.payment.create_payment_intent(100, "test@example.com")
            self.fail("Should have raised PaymentNotEnabledError")
        except PaymentNotEnabledError as e:
            error_str = str(e)
            # Should mention sandbox location
            self.assertIn("sandbox", error_str.lower())


if __name__ == "__main__":
    unittest.main()
