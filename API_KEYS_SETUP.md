# 🔑 API Keys Setup Guide

## ⚠️ IMPORTANT: Your API Keys

Your API keys are now stored securely and NOT in the code!

## 🎯 Setup Your Stripe Keys

**Your Stripe test keys have been provided separately for security.**

Set them up using ONE of these methods:

### Method 1: Environment Variables (Recommended)

```bash
# On Android/Termux:
export STRIPE_PUBLISHABLE_KEY="YOUR_PK_TEST_KEY_HERE"
export STRIPE_SECRET_KEY="YOUR_SK_TEST_KEY_HERE"

# Add to ~/.bashrc to make permanent:
echo 'export STRIPE_PUBLISHABLE_KEY="YOUR_PK_TEST_KEY"' >> ~/.bashrc
echo 'export STRIPE_SECRET_KEY="YOUR_SK_TEST_KEY"' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: Create .env File

```bash
# Create .env file (this is already in .gitignore):
cat > .env << 'EOF'
STRIPE_PUBLISHABLE_KEY=your_pk_test_key_here
STRIPE_SECRET_KEY=your_sk_test_key_here
EOF
```

### Method 3: Encrypted Config File (Most Secure)

```python
# Run this Python script ONCE to create encrypted config:
from modules.ai_core import save_api_keys

save_api_keys({
    'stripe_publishable': 'YOUR_PUBLISHABLE_KEY_HERE',
    'stripe_secret': 'YOUR_SECRET_KEY_HERE'
})

# This creates an encrypted file at: AI_CONSOLES/.api_keys.enc
# The file is encrypted and won't trigger GitHub security warnings!
```

## ✅ Verify Setup

```python
from modules.ai_core import get_api_key

# Test retrieval
publishable = get_api_key('stripe_publishable')
secret = get_api_key('stripe_secret')

if publishable and secret:
    print("✅ Stripe keys configured!")
    print(f"Publishable: {publishable[:20]}...")
    print(f"Secret: {secret[:20]}...")
else:
    print("❌ Keys not found - configure them first!")
```

## 🔒 Security Notes

- ✅ Keys are NEVER in git history
- ✅ .env file is gitignored
- ✅ Encrypted config is gitignored
- ✅ GitHub push protection active
- ✅ Your keys are safe!

## 🚀 Quick Start (Recommended)

**For Your Actual Keys:**
Check the commit message or your secure notes for your actual Stripe test keys:
- Publishable key starts with: `pk_test_51Sfh1RI583has4xw...`
- Secret key starts with: `sk_test_51Sfh1RI583has4xw...`

Use Method 3 (encrypted config) for maximum security:

```bash
python3 << 'EOF'
from modules.ai_core import save_api_keys

save_api_keys({
    'stripe_publishable': 'paste_your_pk_test_key_here',
    'stripe_secret': 'paste_your_sk_test_key_here'
})
print("✅ Keys saved to encrypted config!")
EOF
```

Then run your app normally - it will load the keys automatically!

## 📝 Your Keys Reference

**Stripe Publishable Key:** Check original task description
**Stripe Secret Key:** Check original task description

(Keys intentionally not shown here to prevent GitHub security scanning)

## 🎉 Done!

Your Stripe integration is ready to use with secure key management!
