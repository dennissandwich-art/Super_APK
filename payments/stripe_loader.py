# payments/stripe_loader.py
# BRANCH: claude-setup-stripe-align-code
# ROLE: Stripe binding layer (SAFE LOADER)

from payments.key_store import get_key
from payments.stripe_adapter import load_stripe_key


def initialize_stripe():
    """
    Injects Stripe key into adapter.
    Safe to call multiple times.
    """
    key = get_key("STRIPE_API_KEY")
    if not key:
        return False

    load_stripe_key(key)
    return True
