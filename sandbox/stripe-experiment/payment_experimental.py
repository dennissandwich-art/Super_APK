"""
SANDBOX: Stripe Payment Experiment
==================================
WARNING: THIS CODE IS NOT PRODUCTION READY

CRITICAL ISSUES (DO NOT USE IN PRODUCTION):
1. NO IDEMPOTENCY KEYS - violates Stripe best practices
2. NO REPLAY PROTECTION for webhooks
3. Claims PCI-DSS compliance without implementation
4. Uses test keys only

REQUIRED BEFORE PRODUCTION:
- Add idempotency_key to ALL write operations
- Implement webhook event deduplication
- Add proper secret management (not env vars)
- Security audit by qualified professional
- PCI-DSS compliance validation

See: https://stripe.com/docs/api/idempotent_requests
See: https://stripe.com/docs/webhooks/best-practices
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path

# EXPERIMENTAL - DO NOT IMPORT IN PRODUCTION CODE
PAYMENT_LOGS_DIR = "/sdcard/superapk_payments"
PAYMENT_DB = "/sdcard/superapk_payment_records.json"

# Processed webhook events for replay protection
_processed_events = set()


class StripePaymentExperimental:
    """
    EXPERIMENTAL Stripe Integration

    NOT FOR PRODUCTION USE - Missing:
    - Idempotency keys
    - Proper secret management
    - Webhook replay protection
    - PCI-DSS compliance
    """

    def __init__(self, test_mode=True):
        if not test_mode:
            raise RuntimeError(
                "StripePaymentExperimental cannot run in production mode. "
                "This code lacks required safety features."
            )

        self.stripe_initialized = False
        self.test_mode = True
        self.payment_records = []
        self._init_stripe()

    def _init_stripe(self):
        """Initialize Stripe in TEST MODE ONLY"""
        try:
            import stripe
            self.stripe = stripe

            # ONLY allow test keys
            secret_key = os.environ.get('STRIPE_TEST_SECRET_KEY')
            if not secret_key:
                print("[SANDBOX] No STRIPE_TEST_SECRET_KEY found")
                return

            if not secret_key.startswith('sk_test_'):
                raise RuntimeError(
                    "FATAL: Attempted to use non-test Stripe key in sandbox. "
                    "Only sk_test_* keys are allowed."
                )

            self.stripe.api_key = secret_key
            self.stripe_initialized = True
            print("[SANDBOX] Stripe initialized in TEST MODE")

        except ImportError:
            print("[SANDBOX] Stripe library not installed")

    def _generate_idempotency_key(self, operation, unique_id):
        """
        Generate idempotency key for Stripe operations.

        IMPORTANT: In production, this should be:
        - Deterministic for retries
        - Unique per logical operation
        - Stored for verification
        """
        return f"{operation}_{unique_id}_{datetime.now().strftime('%Y%m%d')}"

    def create_payment_intent_experimental(self, amount_cents, currency='usd',
                                           order_id=None, idempotency_key=None):
        """
        Create payment intent WITH idempotency key.

        Args:
            amount_cents: Amount in smallest currency unit
            currency: Currency code
            order_id: Your order ID for tracking
            idempotency_key: Required for safe retries

        Returns:
            (client_secret, payment_intent_id, error)
        """
        if not self.stripe_initialized:
            return None, None, "Stripe not initialized (test mode)"

        # Generate idempotency key if not provided
        if not idempotency_key:
            idempotency_key = self._generate_idempotency_key(
                'create_pi',
                order_id or uuid.uuid4().hex[:8]
            )

        try:
            payment_intent = self.stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=currency,
                metadata={'order_id': order_id or 'test'},
                idempotency_key=idempotency_key  # CRITICAL: Required for safety
            )

            print(f"[SANDBOX] Created PaymentIntent: {payment_intent.id}")
            print(f"[SANDBOX] Idempotency key: {idempotency_key}")

            return payment_intent.client_secret, payment_intent.id, None

        except self.stripe.error.StripeError as e:
            return None, None, str(e)

    def verify_webhook_with_replay_protection(self, payload, signature,
                                               webhook_secret, event_id=None):
        """
        Verify webhook WITH replay protection.

        IMPORTANT: Production must:
        - Store processed event IDs in persistent storage
        - Handle race conditions
        - Clean up old event IDs periodically
        """
        if not self.stripe_initialized:
            return None, "Stripe not initialized"

        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )

            # Replay protection
            event_id = event.get('id')
            if event_id in _processed_events:
                print(f"[SANDBOX] Duplicate webhook rejected: {event_id}")
                return None, "Duplicate event (replay protection)"

            _processed_events.add(event_id)
            print(f"[SANDBOX] Webhook verified: {event['type']}")

            return event, None

        except ValueError:
            return None, "Invalid payload"
        except self.stripe.error.SignatureVerificationError:
            return None, "Invalid signature"


# Prevent direct import in production code
def _warn_experimental():
    import warnings
    warnings.warn(
        "sandbox.stripe-experiment is EXPERIMENTAL. "
        "Do not use in production without implementing required safety features.",
        UserWarning,
        stacklevel=3
    )

_warn_experimental()
