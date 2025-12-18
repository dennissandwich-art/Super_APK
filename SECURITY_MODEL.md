# Super_APK Security Model

## Overview

This document describes the security measures implemented in Super_APK and, importantly, what is **NOT** implemented.

## What Is Implemented

### 1. Kernel Invariant Enforcement
- Violations crash the application loudly
- Single kernel instance enforced
- Subsystem initialization required before use

### 2. Payment Blocking
- All payment operations are disabled
- Attempting payment raises `PaymentNotEnabledError`
- Experimental code quarantined to `sandbox/stripe-experiment/`

### 3. Secret Exclusion
- `.gitignore` blocks common secret patterns
- `.env`, `*.key`, `credentials.json`, etc. are excluded

### 4. Basic File Permissions
- Storage directories use `0700` permissions
- Storage files use `0600` permissions
- (Effectiveness varies by platform)

## What Is NOT Implemented

### 1. Encryption at Rest
- No encryption of stored data
- Relies on filesystem permissions only
- Android external storage is readable by other apps

### 2. Secure Key Management
- No Android Keystore integration
- `python-keyring` used when available (desktop only)
- **API keys should use environment variables**

### 3. Network Security
- No certificate pinning
- No additional TLS verification
- Relies on system TLS

### 4. Code Obfuscation
- No obfuscation of Python bytecode
- APK can be decompiled

## Secret Management

### Do NOT Store in SecureStorage:
- API keys
- Passwords
- Payment credentials
- OAuth tokens

### Use Instead:
```python
# Environment variables (recommended)
import os
api_key = os.environ.get('API_KEY')

# python-keyring (desktop only)
import keyring
keyring.set_password('superapk', 'api_key', 'value')
```

## Payment Security

Payments are **completely disabled** until:
1. Idempotency keys implemented
2. Webhook replay protection added
3. Proper secret management configured
4. Security audit completed
5. PCI-DSS compliance validated

See `PAYMENT_POLICY.md` for details.

## Reporting Security Issues

If you discover a security vulnerability:
1. Do NOT open a public issue
2. Contact the maintainers privately
3. Allow time for a fix before disclosure
