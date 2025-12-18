# Payment Policy

## Current Status: DISABLED

All payment functionality is **disabled** in this codebase.

Attempting to process payments will raise `PaymentNotEnabledError`.

## Why Payments Are Disabled

The previous payment implementation had critical security issues:

1. **No Idempotency Keys** - Stripe requires idempotency keys to prevent duplicate charges. The implementation had none.

2. **No Webhook Replay Protection** - Webhooks could be replayed, causing duplicate processing.

3. **False Compliance Claims** - The code claimed "PCI-DSS Level 1 Compliance" without evidence.

4. **Custom Crypto** - Used homegrown encryption instead of proper key management.

## Experimental Code Location

Experimental Stripe code is quarantined at:
```
sandbox/stripe-experiment/payment_experimental.py
```

This code:
- Only works with `sk_test_*` keys
- Includes idempotency key generation
- Includes webhook replay protection skeleton
- **Still not production ready**

## Requirements Before Enabling Payments

### 1. Technical Requirements
- [ ] Idempotency keys on ALL write operations
- [ ] Webhook signature verification with construct_event
- [ ] Webhook replay protection (event ID deduplication)
- [ ] Proper error handling and retry logic
- [ ] Background processing for webhooks
- [ ] No coupling to order fulfillment in same transaction

### 2. Security Requirements
- [ ] Secrets in environment variables or secret manager
- [ ] No secrets in code or config files
- [ ] TLS for all connections
- [ ] Audit logging

### 3. Compliance Requirements
- [ ] Security audit by qualified professional
- [ ] PCI-DSS compliance validation (if applicable)
- [ ] Terms of service compliance with Stripe

### 4. Operational Requirements
- [ ] Monitoring and alerting
- [ ] Rollback capability
- [ ] Incident response plan

## References

- [Stripe Idempotent Requests](https://stripe.com/docs/api/idempotent_requests)
- [Stripe Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)
- [Stripe PCI Compliance](https://stripe.com/docs/security/guide)

## Re-enabling Payments

To re-enable payments:

1. Complete ALL requirements above
2. Have code reviewed by security professional
3. Update `payment.py` to actually process payments
4. Remove `PaymentNotEnabledError` checks
5. Add comprehensive integration tests
6. Document compliance evidence
