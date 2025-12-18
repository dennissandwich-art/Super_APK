"""
NTRLI SuperAPK - Payment Module Stub
=====================================

PAYMENTS ARE NOT ENABLED

This is a stub module. Real payment processing requires:
1. Security audit
2. PCI-DSS compliance validation
3. Proper secret management
4. Idempotency implementation
5. Webhook replay protection

For experimental Stripe code, see: sandbox/stripe-experiment/

DO NOT enable payments without completing the above requirements.
"""


class PaymentNotEnabledError(Exception):
    """Raised when attempting to use disabled payment functionality."""
    pass


class PaymentManager:
    """
    Payment manager stub.

    All payment operations are disabled until security requirements are met.
    """

    def __init__(self, *args, **kwargs):
        self._enabled = False

    def _raise_not_enabled(self):
        raise PaymentNotEnabledError(
            "Payment processing is not enabled. "
            "See sandbox/stripe-experiment/ for development. "
            "Production requires security audit and PCI-DSS compliance."
        )

    def create_payment_intent(self, *args, **kwargs):
        """Disabled: Payment creation not enabled."""
        self._raise_not_enabled()

    def confirm_payment(self, *args, **kwargs):
        """Disabled: Payment confirmation not enabled."""
        self._raise_not_enabled()

    def process_payment(self, *args, **kwargs):
        """Disabled: Payment processing not enabled."""
        self._raise_not_enabled()

    def is_enabled(self):
        """Check if payments are enabled."""
        return False


# Alias for backwards compatibility - will raise on use
StripePaymentManager = PaymentManager


def get_payment_manager(*args, **kwargs):
    """Get payment manager instance (stub)."""
    return PaymentManager()
