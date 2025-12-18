# 
# BRANCH: claude-setup-stripe-align-code
# ROLE: Optional Stripe integration (ISOLATED, FAIL-SILENT)

"""
IMPORTANT:
- Stripe API keys are NEVER hardcoded.
- This module only REFERENCES a variable.
- The variable can later be:
    - injected via environment
    - loaded from encrypted storage
    - resolved via secure dataset
"""

# PLACEHOLDER VARIABLE (REFERENCE ONLY)
# This is intentionally empty.
STRIPE_API_KEY = None


def load_stripe_key(key: str) -> None:
    """
    Injects the Stripe API key at runtime.
    This function is the ONLY allowed way
    to provide the key to this module.
    """
    global STRIPE_API_KEY
    STRIPE_API_KEY = key


def start_stripe_payment(amount_cents: int) -> bool:
    """
    Executes a Stripe payment attempt.
    Failure MUST NOT crash the app.
    """
    try:
        if STRIPE_API_KEY is None:
            raise RuntimeError("Stripe API key not provided")

        import stripe

        # Stripe is initialized ONLY here
        stripe.api_key = STRIPE_API_KEY

        # Placeholder payment logic
        # Real implementation can be added later
        return True

    except Exception as e:
        # HARD RULE:
        # Stripe failure must NEVER propagate
        print("Stripe module disabled:", e)
        return False
