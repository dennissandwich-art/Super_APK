"""
NTRLI SuperAPK - Stripe Payment Integration Module
PCI-DSS Compliant Payment Processing
Phase 3: Secure payment gateway with 3D Secure support
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Import encrypted key retrieval
try:
    from modules.ai_core import get_api_key, AI_CONSOLE
except ImportError:
    from ai_core import get_api_key, AI_CONSOLE

PAYMENT_LOGS_DIR = "/sdcard/superapk_payments"
PAYMENT_DB = "/sdcard/superapk_payment_records.json"

class StripePaymentManager:
    """
    PCI-DSS Level 1 Compliant Stripe Integration
    - Card data never touches the server
    - 3D Secure authentication enforced
    - Full audit logging
    - Webhook verification
    """

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.stripe_initialized = False
        self.payment_records = self._load_payment_records()
        self._ensure_logs_dir()

        # Initialize Stripe with encrypted keys
        try:
            import stripe
            self.stripe = stripe

            # Load encrypted Stripe secret key
            secret_key = get_api_key('stripe_secret')
            if not secret_key:
                self.log("Stripe secret key not found - payments disabled", "ERROR")
                return

            self.stripe.api_key = secret_key
            self.publishable_key = get_api_key('stripe_publishable')
            self.stripe_initialized = True

            self.log("Stripe payment gateway initialized (Test Mode)")
            self.log(f"Publishable key: {self.publishable_key[:20]}...")

        except ImportError:
            self.log("Stripe library not installed - run: pip install stripe", "ERROR")
        except Exception as e:
            self.log(f"Failed to initialize Stripe: {e}", "ERROR")

    def log(self, msg, level="INFO"):
        """Enhanced logging with AI console"""
        if self.ai_console:
            self.ai_console.log(f"[PAYMENT] {msg}", level)
        else:
            print(f"[PAYMENT] {msg}")

        # Also log to payment-specific log
        try:
            log_file = os.path.join(PAYMENT_LOGS_DIR, f"payment_{datetime.now().strftime('%Y%m%d')}.log")
            timestamp = datetime.now().isoformat()
            with open(log_file, "a") as f:
                f.write(f"[{timestamp}] [{level}] {msg}\n")
        except Exception as e:
            print(f"Failed to write payment log: {e}")

    def _ensure_logs_dir(self):
        """Ensure payment logs directory exists"""
        try:
            Path(PAYMENT_LOGS_DIR).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log(f"Error creating payment logs dir: {e}", "ERROR")

    def _load_payment_records(self):
        """Load payment records database"""
        try:
            if os.path.exists(PAYMENT_DB):
                with open(PAYMENT_DB, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.log(f"Error loading payment records: {e}", "ERROR")
            return []

    def _save_payment_records(self):
        """Save payment records database"""
        try:
            Path(PAYMENT_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(PAYMENT_DB, "w") as f:
                json.dump(self.payment_records, f, indent=2)
        except Exception as e:
            self.log(f"Error saving payment records: {e}", "ERROR")

    def _record_payment(self, payment_data):
        """Record payment for audit trail"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "payment_intent_id": payment_data.get("id"),
            "amount": payment_data.get("amount"),
            "currency": payment_data.get("currency"),
            "status": payment_data.get("status"),
            "order_id": payment_data.get("metadata", {}).get("order_id")
        }
        self.payment_records.append(record)
        self._save_payment_records()
        self.log(f"Payment recorded: {record['payment_intent_id']}")

    def get_publishable_key(self):
        """Get publishable key for client-side"""
        return self.publishable_key

    def create_payment_intent(self, amount_nok, customer_email=None, order_id=None, metadata=None):
        """
        Create a PaymentIntent for processing payment

        Args:
            amount_nok: Amount in Norwegian Kroner (NOK)
            customer_email: Customer email for receipt
            order_id: Associated order ID
            metadata: Additional metadata

        Returns:
            (client_secret, payment_intent_id, error)
        """
        if not self.stripe_initialized:
            return None, None, "Stripe not initialized"

        try:
            # Convert NOK to øre (smallest currency unit)
            amount_ore = int(amount_nok * 100)

            # Prepare metadata
            payment_metadata = {
                "app": "Super_APK",
                "order_id": order_id or f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "created_at": datetime.now().isoformat()
            }
            if metadata:
                payment_metadata.update(metadata)

            self.log(f"Creating payment intent: {amount_nok} NOK")

            # Create PaymentIntent with 3D Secure enforcement
            payment_intent = self.stripe.PaymentIntent.create(
                amount=amount_ore,
                currency='nok',
                receipt_email=customer_email,
                metadata=payment_metadata,
                # Automatic payment methods (includes card, Apple Pay, Google Pay)
                automatic_payment_methods={'enabled': True},
                # Enforce Strong Customer Authentication (SCA)
                payment_method_options={
                    'card': {
                        'request_three_d_secure': 'any'  # Always request 3DS
                    }
                },
                # Capture method
                capture_method='automatic'
            )

            # Record the payment intent
            self._record_payment(payment_intent)

            self.log(f"Payment intent created: {payment_intent.id}")
            self.log(f"Amount: {amount_nok} NOK ({amount_ore} øre)")

            return payment_intent.client_secret, payment_intent.id, None

        except self.stripe.error.CardError as e:
            # Card was declined
            error_msg = f"Card declined: {e.user_message}"
            self.log(error_msg, "ERROR")
            return None, None, error_msg

        except self.stripe.error.InvalidRequestError as e:
            error_msg = f"Invalid request: {str(e)}"
            self.log(error_msg, "ERROR")
            return None, None, error_msg

        except Exception as e:
            error_msg = f"Payment creation failed: {str(e)}"
            self.log(error_msg, "ERROR")
            return None, None, error_msg

    def confirm_payment(self, payment_intent_id, payment_method_id=None):
        """
        Confirm a payment intent

        Args:
            payment_intent_id: The payment intent ID
            payment_method_id: Optional payment method ID

        Returns:
            (success, payment_intent, error)
        """
        if not self.stripe_initialized:
            return False, None, "Stripe not initialized"

        try:
            self.log(f"Confirming payment: {payment_intent_id}")

            kwargs = {'return_url': 'https://superapk.org/payment/complete'}
            if payment_method_id:
                kwargs['payment_method'] = payment_method_id

            payment_intent = self.stripe.PaymentIntent.confirm(
                payment_intent_id,
                **kwargs
            )

            self.log(f"Payment confirmed: {payment_intent.id} - Status: {payment_intent.status}")

            # Update payment record
            self._record_payment(payment_intent)

            return True, payment_intent, None

        except Exception as e:
            error_msg = f"Payment confirmation failed: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, None, error_msg

    def retrieve_payment(self, payment_intent_id):
        """
        Retrieve payment intent details

        Args:
            payment_intent_id: The payment intent ID

        Returns:
            (payment_intent, error)
        """
        if not self.stripe_initialized:
            return None, "Stripe not initialized"

        try:
            payment_intent = self.stripe.PaymentIntent.retrieve(payment_intent_id)
            self.log(f"Retrieved payment: {payment_intent_id} - Status: {payment_intent.status}")
            return payment_intent, None
        except Exception as e:
            error_msg = f"Failed to retrieve payment: {str(e)}"
            self.log(error_msg, "ERROR")
            return None, error_msg

    def cancel_payment(self, payment_intent_id):
        """
        Cancel a payment intent

        Args:
            payment_intent_id: The payment intent ID

        Returns:
            (success, error)
        """
        if not self.stripe_initialized:
            return False, "Stripe not initialized"

        try:
            payment_intent = self.stripe.PaymentIntent.cancel(payment_intent_id)
            self.log(f"Payment cancelled: {payment_intent_id}")
            self._record_payment(payment_intent)
            return True, None
        except Exception as e:
            error_msg = f"Failed to cancel payment: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg

    def create_refund(self, payment_intent_id, amount_nok=None, reason=None):
        """
        Create a refund for a payment

        Args:
            payment_intent_id: The payment intent ID to refund
            amount_nok: Optional partial refund amount in NOK
            reason: Reason for refund (duplicate, fraudulent, requested_by_customer)

        Returns:
            (refund, error)
        """
        if not self.stripe_initialized:
            return None, "Stripe not initialized"

        try:
            kwargs = {'payment_intent': payment_intent_id}

            if amount_nok:
                kwargs['amount'] = int(amount_nok * 100)

            if reason:
                kwargs['reason'] = reason

            refund = self.stripe.Refund.create(**kwargs)

            self.log(f"Refund created: {refund.id} for payment {payment_intent_id}")
            return refund, None

        except Exception as e:
            error_msg = f"Refund failed: {str(e)}"
            self.log(error_msg, "ERROR")
            return None, error_msg

    def verify_webhook(self, payload, signature, webhook_secret):
        """
        Verify Stripe webhook signature

        Args:
            payload: Request body
            signature: Stripe-Signature header
            webhook_secret: Webhook signing secret

        Returns:
            (event, error)
        """
        if not self.stripe_initialized:
            return None, "Stripe not initialized"

        try:
            event = self.stripe.Webhook.construct_event(
                payload, signature, webhook_secret
            )
            self.log(f"Webhook verified: {event['type']}")
            return event, None
        except ValueError as e:
            return None, "Invalid payload"
        except self.stripe.error.SignatureVerificationError as e:
            return None, "Invalid signature"

    def get_payment_history(self, limit=50):
        """Get payment history"""
        return self.payment_records[-limit:]

    def get_payment_stats(self):
        """Get payment statistics"""
        total_payments = len(self.payment_records)
        total_amount = sum(r.get('amount', 0) for r in self.payment_records) / 100  # Convert from øre

        successful = len([r for r in self.payment_records if r.get('status') == 'succeeded'])
        failed = len([r for r in self.payment_records if r.get('status') in ['failed', 'canceled']])

        return {
            'total_payments': total_payments,
            'total_amount_nok': total_amount,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total_payments * 100) if total_payments > 0 else 0
        }

    def test_connection(self):
        """Test Stripe API connection"""
        if not self.stripe_initialized:
            return False, "Stripe not initialized"

        try:
            # Try to retrieve balance (test endpoint)
            balance = self.stripe.Balance.retrieve()
            self.log(f"Stripe connection OK - Account has {len(balance.available)} currency balances")
            return True, None
        except Exception as e:
            error_msg = f"Stripe connection test failed: {str(e)}"
            self.log(error_msg, "ERROR")
            return False, error_msg
