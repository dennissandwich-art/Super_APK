# payments/stripe_impl.py
# BRANCH: claude-setup-stripe-align-code
# ROLE: Stripe implementation (FAIL-SILENT)

from payments.stripe_contract import StripeContract
from payments.stripe_loader import initialize_stripe
from payments.stripe_adapter import start_stripe_payment


class StripeService(StripeContract):
    def initialize(self) -> bool:
        return initialize_stripe()

    def charge(self, amount_cents: int) -> bool:
        return start_stripe_payment(amount_cents)
