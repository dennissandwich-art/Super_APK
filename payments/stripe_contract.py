# payments/stripe_contract.py
# BRANCH: claude-setup-stripe-align-code
# ROLE: Stripe interface contract (NO SIDE EFFECTS)

"""
This file defines how the kernel may talk to Stripe.
No Stripe imports allowed here.
"""

class StripeContract:
    def initialize(self) -> bool:
        raise NotImplementedError

    def charge(self, amount_cents: int) -> bool:
        raise NotImplementedError
