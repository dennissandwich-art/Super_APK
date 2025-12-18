# NTRLI SuperAPK - Complete Build Guide

## 📱 Phone-Only Android APK Build System

This is the **complete, production-ready** SuperAPK build system with:
- ✅ Incremental phase-based deployment
- ✅ AI self-healing and monitoring
- ✅ Lazy module loading
- ✅ Crash-safe architecture
- ✅ Full dependency management
- ✅ Phone-only build (no PC required)

---

## 🚀 Quick Start

### Prerequisites

**On your Android device (5.0+):**

1. **Termux** (install from F-Droid)
2. **Python 3.11.8**
3. **Git**

```bash
# In Termux
pkg update && pkg upgrade
pkg install python git build-essential libffi openssl
```

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd SuperAPK

# Make setup script executable
chmod +x setup.sh

# Run Phase 0 setup
./setup.sh all
```

---

## 📦 Project Structure

```
SuperAPK/
├── app1/
│   ├── main.py                 # Core app with AI self-healing
│   ├── buildozer.spec          # Build configuration
│   ├── modules/
│   │   ├── auth.py            # Authentication (Phase 1)
│   │   ├── network.py         # Network & Tor (Phase 1)
│   │   ├── news.py            # News feed (Phase 2)
│   │   ├── ecommerce.py       # E-commerce (Phase 2)
│   │   ├── ai.py              # Claude + GPT-4 (Phase 3)
│   │   ├── admin.py           # Admin panel (Phase 3)
│   │   └── i18n.py            # Multi-language (Phase 3)
│   └── assets/
│       └── icon.png
├── setup.sh                    # Build automation
└── README.md
```

---

## 🔄 Phased Deployment

### **Phase 0: Minimal Stable** ✅

**Features:**
- Basic UI with branding
- "Get Started" and "Settings" buttons
- Crash logging to `/sdcard/superbot_crash.log`
- AI console logging to `/sdcard/AI_consoles_main.log`
- Self-healing routine

**Dependencies:**
- python3==3.11.8
- kivy==2.3.1
- kivymd==1.1.1

**Setup:**
```bash
./setup.sh 0
```

**Test:**
```bash
cd app1
python main.py
# Verify UI loads, buttons work, logs created
```

**Build APK:**
```bash
./setup.sh build
```

---

### **Phase 1: Authentication & Network** 🔐

**Features:**
- Internal authentication system
- User registration/login
- Session management
- Admin user: `Sir_NTRLI_II`
- Tor/VPN proxy support
- Network health monitoring

**Dependencies:**
- requests==2.31.0
- pysocks==1.7.1
- cryptography==41.0.7

**Permissions:**
- INTERNET
- ACCESS_NETWORK_STATE
- WRITE_EXTERNAL_STORAGE
- READ_EXTERNAL_STORAGE

**Setup:**
```bash
./setup.sh 1
```

**Test:**
```bash
cd app1
python -c "
from modules.auth import AuthManager
from modules.network import NetworkManager

auth = AuthManager()
print('Login test:', auth.login('Sir_NTRLI_II', 'NTRLI_ADMIN_2024'))

net = NetworkManager()
print('Network test:', net.check_connectivity())
"
```

---

### **Phase 2: News & E-commerce** 📰🛒

**Features:**
- Business news feed aggregator
- Product catalog with 5+ sample products
- Shopping cart
- 400 NOK minimum order enforcement
- Order management

**Dependencies:**
- feedparser==6.0.10
- pillow==10.2.0
- sqlalchemy==2.0.25

**Permissions:**
- POST_NOTIFICATIONS

**Setup:**
```bash
./setup.sh 2
```

**Test:**
```bash
cd app1
python -c "
from modules.news import NewsManager
from modules.ecommerce import EcommerceManager

news = NewsManager()
articles = news.fetch_all_feeds()
print(f'Fetched {len(articles)} articles')

shop = EcommerceManager()
products = shop.get_products()
print(f'Products: {len(products)}')
shop.add_to_cart('prod_001', 2)
print(f'Cart total: {shop.get_cart_total()} NOK')
"
```

---

### **Phase 3: AI & Admin** 🤖👑

**Features:**
- Claude API integration
- GPT-4 API integration
- Multi-model AI queries
- AI conversation logging
- Admin panel for `@Sir_NTRLI_II`
- System statistics
- User/product/order management
- Multi-language support (English, Norwegian, Spanish, French)

**Dependencies:**
- flask==3.0.2
- anthropic==0.18.0
- openai==1.12.0
- babel==2.14.0

**Environment Variables:**
```bash
export ANTHROPIC_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

**Setup:**
```bash
./setup.sh 3
```

**Test:**
```bash
cd app1
python -c "
from modules.ai import AIManager
from modules.admin import AdminManager
from modules.i18n import I18nManager

# AI test (requires API keys)
ai = AIManager()
response, error = ai.query_claude('Hello, Claude!')
print('AI response:', response)

# Admin test
admin = AdminManager()
stats = admin.get_system_stats()
print('System stats:', stats)

# i18n test
i18n = I18nManager()
print('English:', i18n.t('app_title'))
i18n.set_language('no')
print('Norwegian:', i18n.t('app_title'))
"
```

---

## 🛠️ Build Commands

### Clean Build Environment
```bash
./setup.sh clean
```

### Setup Specific Phase
```bash
./setup.sh 0  # Phase 0
./setup.sh 1  # Phase 1
./setup.sh 2  # Phase 2
./setup.sh 3  # Phase 3
```

### Build APK
```bash
./setup.sh build
```

### Run Tests
```bash
./setup.sh test
```

---

## 📊 AI Self-Healing System

The app includes an **AI self-healing routine** that runs at startup:

**Features:**
- Validates all module files exist
- Checks Python dependencies
- Monitors system health
- Logs all checks to AI console
- Attempts auto-recovery on failures

**Logs Location:**
- Main log: `/sdcard/AI_consoles_main.log`
- Crash log: `/sdcard/superbot_crash.log`
- AI interaction logs: `/sdcard/AI_consoles/ai_interaction_*.json`
- Admin logs: `/sdcard/superapk_admin_logs.json`

**Monitoring:**
```bash
# View main log
tail -f /sdcard/AI_consoles_main.log

# View crash log
tail -f /sdcard/superbot_crash.log

# View AI interactions
ls -lh /sdcard/AI_consoles/
```

---

## 🔐 Admin Access

**Default Admin Credentials:**
- Username: `Sir_NTRLI_II`
- Password: `NTRLI_ADMIN_2024`

**Admin Capabilities:**
- View system statistics
- Manage users (create, delete, promote)
- Manage products (create, delete, update stock)
- Manage orders (update status, cancel)
- Export system data
- View all logs

---

## 🌍 Multi-Language Support

**Available Languages:**
- English (en) - default
- Norwegian (no)
- Spanish (es)
- French (fr)

**Add New Language:**
```python
from modules.i18n import I18nManager

i18n = I18nManager()
i18n.add_language("de", {
    "app_title": "NTRLI SuperAPK",
    "get_started": "Loslegen",
    # ... more translations
})
```

---

## 🐛 Troubleshooting

### Build Fails

1. **Check logs:**
```bash
./setup.sh test
cat /sdcard/superbot_crash.log
cat /sdcard/AI_consoles_main.log
```

2. **Clean and rebuild:**
```bash
./setup.sh clean
./setup.sh 0
./setup.sh build
```

3. **Verify dependencies:**
```bash
pip3 list | grep -E "(kivy|requests|anthropic)"
```

### Module Import Errors

**Symptom:** `ModuleNotFoundError` when running app

**Solution:**
```bash
# Ensure all modules are in place
ls -l app1/modules/

# Verify Python can import
cd app1
python -c "from modules.auth import AuthManager"
```

### API Key Issues

**Symptom:** AI features not working

**Solution:**
```bash
# Set environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Or add to .bashrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚨 Emergency Rollback

If a phase fails:

1. **Comment out new modules in main.py:**
```python
# self.lazy_load("modules.ai")  # Disable Phase 3
```

2. **Revert buildozer.spec dependencies:**
```bash
# Edit buildozer.spec
# Remove problematic dependencies
```

3. **Rebuild:**
```bash
./setup.sh clean
./setup.sh build
```

4. **Analyze logs:**
```bash
./setup.sh test
```

---

## 📱 APK Installation

After successful build:

```bash
# APK location
ls -lh app1/bin/*.apk

# Install on device
adb install app1/bin/superapk-1.0.10-debug.apk

# Or copy to device storage and install manually
cp app1/bin/*.apk /sdcard/Download/
```

---

## 🔬 Testing Checklist

### Phase 0 ✅
- [ ] App launches without crash
- [ ] UI displays correctly
- [ ] "Get Started" button works
- [ ] "Settings" button works
- [ ] Crash log created
- [ ] AI console log created
- [ ] Self-healing routine executes

### Phase 1 ✅
- [ ] User registration works
- [ ] Login works
- [ ] Session persists
- [ ] Admin login works
- [ ] Network connectivity check works
- [ ] Auth logs generated

### Phase 2 ✅
- [ ] News feed loads
- [ ] Products display
- [ ] Add to cart works
- [ ] Cart total calculates correctly
- [ ] 400 NOK minimum enforced
- [ ] Checkout process works

### Phase 3 ✅
- [ ] Claude API responds
- [ ] GPT-4 API responds
- [ ] Admin panel accessible
- [ ] System stats display
- [ ] Multi-language switching works
- [ ] All AI interactions logged

---

## 📞 Support

**Admin Contact:** @Sir_NTRLI_II on Telegram

**Issue Reporting:**
1. Check `/sdcard/superbot_crash.log`
2. Check `/sdcard/AI_consoles_main.log`
3. Run `./setup.sh test`
4. Report with logs to admin

---

## 📄 License

Proprietary - NTRLI Organization

---

## 🎯 Next Steps

1. **Complete Phase 0** → Test thoroughly
2. **Enable Phase 1** → Verify auth/network
3. **Enable Phase 2** → Test shopping flow
4. **Enable Phase 3** → Configure API keys
5. **Build final APK** → Deploy to users

---

**Built with ❤️ by NTRLI for Android phones everywhere.**
