# payments/stripe_entry.py
# BRANCH: claude-setup-stripe-align-code
# ROLE: Kernel-aware Stripe entrypoint

from payments.stripe_impl import StripeService


def try_initialize_stripe(kernel) -> bool:
    """
    Stripe may only initialize if kernel allows it.
    """
    if not kernel.is_feature_enabled("FEATURE_STRIPE"):
        return False

    service = StripeService()
    return service.initialize()
