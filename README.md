# NTRLI SuperAPK 🚀

**AI-Powered Business Platform for Android**

A comprehensive mobile business platform featuring e-commerce with Stripe payments, AI integration (Claude & GPT-4), news aggregation, secure authentication, network management, and admin controls.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Building the APK](#building-the-apk)
- [Phase Development](#phase-development)
- [API Keys Setup](#api-keys-setup)
- [Stripe Integration](#stripe-integration)
- [Modules Documentation](#modules-documentation)
- [Admin Panel](#admin-panel)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Features (Phase 0)
- ✅ Kivy/KivyMD UI framework
- ✅ AI self-healing crash detection
- ✅ Comprehensive logging system
- ✅ Lazy module loading
- ✅ Dark theme UI

### Authentication & Network (Phase 1)
- ✅ User registration & login
- ✅ Session management (7-day validity)
- ✅ Admin role system (@Sir_NTRLI_II)
- ✅ Tor/VPN proxy support
- ✅ Network health monitoring

### E-commerce & News (Phase 2)
- ✅ Product catalog management
- ✅ Shopping cart with 400 NOK minimum order
- ✅ **Stripe payment integration**
  - Payment Intents API
  - Checkout Sessions
  - Payment confirmation
  - Refund support
- ✅ RSS news aggregation
- ✅ Multi-source news feeds
- ✅ Category filtering

### AI & Admin (Phase 3)
- ✅ Multi-model AI support (Claude & GPT-4)
- ✅ Conversation history
- ✅ Sentiment analysis
- ✅ Business insights generation
- ✅ Complete admin dashboard
- ✅ Multi-language support (EN, NO, ES, FR)

---

## 📁 Project Structure

```
Super_APK/
├── main.py                 # Main application entry point
├── buildozer.spec         # Android build configuration
├── setup.sh               # Automated build script
├── .env.example           # Environment variables template
├── README.md              # This file
├── modules/
│   ├── __init__.py
│   ├── auth.py           # Authentication & session management
│   ├── network.py        # Network & Tor/VPN connectivity
│   ├── ecommerce.py      # Shopping cart & Stripe payments
│   ├── news.py           # News feed aggregation
│   ├── ai.py             # AI integrations (Claude, GPT-4)
│   ├── admin.py          # Admin panel & monitoring
│   └── i18n.py           # Internationalization
└── assets/
    └── icon.png          # App icon
```

---

## 🚀 Installation

### Prerequisites

- Android device or emulator
- Python 3.11.8
- Buildozer (for APK building)
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/dennissandwich-art/Super_APK.git
cd Super_APK

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Make setup script executable
chmod +x setup.sh

# Run Phase 0 setup (minimal stable)
./setup.sh all

# Build APK
./setup.sh build
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then fill in your API keys:

```env
# Stripe (Required for payments)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# AI APIs (Optional but recommended)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
MISTRAL_API_KEY=ag_...
```

### Admin Access

Default admin account:
- **Username:** `Sir_NTRLI_II`
- **Password:** `NTRLI_ADMIN_2024`

⚠️ **Change this password in production!**

---

## 📦 Building the APK

### Using setup.sh

```bash
# Phase 0 - Minimal stable core
./setup.sh 0

# Phase 1 - Auth & Network
./setup.sh 1

# Phase 2 - E-commerce & News (includes Stripe)
./setup.sh 2

# Phase 3 - AI & Admin
./setup.sh 3

# Build the APK
./setup.sh build

# Clean build environment
./setup.sh clean

# Run tests
./setup.sh test
```

### Manual Build

```bash
# Install buildozer
pip install buildozer

# Build debug APK
buildozer android debug

# Build release APK (signed)
buildozer android release
```

APK output location: `./bin/superapk-*.apk`

---

## 🔄 Phase Development

### Phase 0: Minimal Stable Core
**Status:** ✅ Complete

Dependencies:
- python3==3.11.8
- kivy==2.3.1
- kivymd==1.1.1

Features:
- Basic UI
- Crash handling
- AI console logging
- Self-healing system checks

### Phase 1: Authentication & Network
**Status:** ✅ Complete

Dependencies:
- requests==2.31.0
- pysocks==1.7.1
- cryptography==41.0.7

Features:
- User authentication
- Session management
- Tor/VPN support
- Network health checks

### Phase 2: E-commerce & News
**Status:** ✅ Complete (with Stripe!)

Dependencies:
- feedparser==6.0.10
- pillow==10.2.0
- sqlalchemy==2.0.25
- **stripe==7.0.0** ⭐

Features:
- Product catalog
- Shopping cart (400 NOK minimum)
- **Stripe payment processing**
- News aggregation
- Multi-source feeds

### Phase 3: AI & Admin
**Status:** ✅ Complete

Dependencies:
- flask==3.0.2
- anthropic==0.18.0
- openai==1.12.0
- babel==2.14.0

Features:
- Claude & GPT-4 integration
- Multi-model AI queries
- Admin dashboard
- Multi-language support

---

## 💳 Stripe Integration

### Setup

1. **Get Stripe API keys:**
   - Visit [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
   - Copy your test keys (for development)
   - Add to `.env` file

2. **Test Mode:**
   - Use test card: `4242 4242 4242 4242`
   - Any future expiry date
   - Any 3-digit CVC

### Usage in Code

```python
from modules.ecommerce import EcommerceManager

# Initialize
ecommerce = EcommerceManager(ai_console)

# Method 1: Payment Intent (for custom checkout)
success, order = ecommerce.checkout(
    user_info={"username": "user123"},
    payment_method="stripe"
)
# Use order["payment_client_secret"] on frontend

# Method 2: Checkout Session (hosted checkout page)
success, result = ecommerce.checkout_with_stripe(
    user_info={"username": "user123"},
    success_url="https://yourapp.com/success",
    cancel_url="https://yourapp.com/cancel"
)
# Redirect user to result["checkout_url"]

# Confirm payment
success, msg = ecommerce.confirm_order_payment(order_id)
```

### Stripe Features Implemented

- ✅ Payment Intents API
- ✅ Checkout Sessions (hosted pages)
- ✅ Payment status tracking
- ✅ Automatic currency conversion (NOK)
- ✅ Refund support
- ✅ Metadata tracking
- ✅ Order confirmation

---

## 📚 Modules Documentation

### Authentication Module (`modules/auth.py`)

```python
from modules.auth import AuthManager

auth = AuthManager(ai_console)

# Register user
success, msg = auth.register_user("username", "password")

# Login
success, token, msg = auth.login("username", "password")

# Validate session
valid, session = auth.validate_session(token)

# Check admin
is_admin = auth.is_admin(token)
```

### E-commerce Module (`modules/ecommerce.py`)

```python
from modules.ecommerce import EcommerceManager

ecommerce = EcommerceManager(ai_console)

# Get products
products = ecommerce.get_products(category="services")

# Add to cart
success, msg = ecommerce.add_to_cart("prod_001", quantity=2)

# Checkout with Stripe
success, order = ecommerce.checkout(user_info, payment_method="stripe")
```

### AI Module (`modules/ai.py`)

```python
from modules.ai import AIManager

ai = AIManager(ai_console)

# Query Claude
response, error = ai.query_claude("What is the best business strategy?")

# Query GPT-4
response, error = ai.query_gpt4("Analyze this data")

# Sentiment analysis
sentiment = ai.analyze_sentiment("This product is amazing!")
```

### Network Module (`modules/network.py`)

```python
from modules.network import NetworkManager

network = NetworkManager(ai_console)

# Check connectivity
connected, msg = network.check_connectivity()

# Enable Tor
success, msg = network.enable_tor_proxy()

# Make request through Tor
success, response = network.make_request("https://example.com")
```

### News Module (`modules/news.py`)

```python
from modules.news import NewsManager

news = NewsManager(ai_console, network_manager)

# Fetch all news
articles = news.fetch_all_feeds()

# Get by category
tech_news = news.fetch_all_feeds(category="technology")

# Search
results = news.search_articles("AI business")
```

### Admin Module (`modules/admin.py`)

```python
from modules.admin import AdminManager

admin = AdminManager(ai_console, auth, ecommerce, news, ai)

# Verify admin
if admin.verify_admin(session_token):
    # Get system stats
    stats = admin.get_system_stats()

    # Manage users
    admin.manage_user("promote_admin", "username")

    # Manage products
    admin.manage_product("update_stock", "prod_001", stock=50)
```

---

## 🛡️ Admin Panel

### Access

Only accessible with admin privileges (@Sir_NTRLI_II by default).

### Features

- **System Statistics:** Users, orders, revenue, products
- **User Management:** Promote, demote, delete users
- **Product Management:** Create, update, delete products
- **Order Management:** Update status, cancel orders
- **Data Export:** Export users, products, orders, logs
- **Logs:** View admin activity logs

---

## 🔒 Security

### Best Practices Implemented

✅ **API Keys via Environment Variables**
- Never hardcode API keys
- Use `.env` file (gitignored)
- Secure key storage

✅ **Password Hashing**
- SHA256 hashing
- Secure session tokens
- 7-day session expiry

✅ **Input Validation**
- Stock checking
- Minimum order validation
- User role verification

✅ **Payment Security**
- Stripe PCI compliance
- Secure token handling
- Server-side validation

### Security Checklist

- [ ] Change default admin password
- [ ] Set up production Stripe keys
- [ ] Enable HTTPS for all API calls
- [ ] Review file permissions on Android
- [ ] Implement rate limiting
- [ ] Add payment webhooks

---

## 🐛 Troubleshooting

### Common Issues

**1. Build fails with "command not found"**
```bash
pip install --user buildozer
pip install --user cython
```

**2. Stripe import error**
```bash
pip install stripe==7.0.0
```

**3. Permission denied on Android**
- Check `buildozer.spec` permissions
- Grant storage permissions in Android settings

**4. API keys not working**
- Verify `.env` file exists
- Check environment variable names
- Restart app after changing .env

**5. Crash logs**
- Check `/sdcard/superbot_crash.log`
- Check `/sdcard/AI_consoles_main.log`

---

## 📝 Logs

The app creates several log files on `/sdcard/`:

- `superbot_crash.log` - Crash reports
- `AI_consoles_main.log` - Main app logs
- `AI_consoles/ai_interaction_*.json` - AI interaction logs
- `superapk_*.json` - Data persistence files

---

## 🤝 Contributing

This is a private project for @Sir_NTRLI_II. For support or inquiries, contact the repository owner.

---

## 📄 License

Proprietary - All rights reserved.

---

## 🙏 Credits

- **Framework:** Kivy & KivyMD
- **Payment Processing:** Stripe
- **AI Models:** Anthropic Claude, OpenAI GPT-4
- **Admin:** @Sir_NTRLI_II

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Check logs: `/sdcard/superbot_crash.log`
- Review documentation above

---

**Version:** 1.0.10
**Last Updated:** December 2025
**Status:** ✅ Production Ready (with Stripe Integration!)
