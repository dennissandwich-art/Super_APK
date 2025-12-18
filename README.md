# NTRLI Super_APK

An Android application built with Kivy/KivyMD.

## Status

This codebase is under active development. Some features are implemented, others are planned.

## What Works

- **Application Kernel** - Singleton execution authority with invariant enforcement
- **State Management** - Redux-style centralized state
- **Authentication** - User registration, login, session management
- **News Feed** - RSS feed aggregation
- **E-commerce** - Product catalog, cart (payments disabled)
- **Offline Queue** - Operation queuing for offline-first architecture
- **Monitoring** - Basic performance and event tracking

## What Does NOT Work

- **Payments** - Completely disabled for security reasons (see `PAYMENT_POLICY.md`)
- **Push Notifications** - Not implemented
- **Encryption at Rest** - Not implemented (see `SECURITY_MODEL.md`)

## Project Structure

```
Super_APK/
├── main.py              # Application entry point
├── app_kernel.py        # Kernel (singleton, invariant enforcement)
├── state_manager.py     # Redux-style state management
├── auth.py              # Authentication
├── network.py           # Network operations
├── ecommerce.py         # E-commerce (cart, products)
├── payment.py           # Payment stub (DISABLED)
├── offline_manager.py   # Offline operation queue
├── secure_storage.py    # Data storage
├── monitoring.py        # Performance tracking
├── modules/             # Additional modules
├── tests/               # Unit tests
├── sandbox/             # Experimental code (not for production)
│   └── stripe-experiment/
└── docs/
    ├── ARCHITECTURE.md
    ├── SECURITY_MODEL.md
    └── PAYMENT_POLICY.md
```

## Quick Start

### Prerequisites

- Python 3.8+
- Kivy/KivyMD

### Installation

```bash
# Clone repository
git clone <repo-url>
cd Super_APK

# Install dependencies
pip install kivy kivymd requests

# Run tests
cd tests
./run_tests.sh

# Run application
cd ..
python main.py
```

## Documentation

- **Architecture**: See `ARCHITECTURE.md`
- **Security**: See `SECURITY_MODEL.md`
- **Payments**: See `PAYMENT_POLICY.md` (disabled)

## Testing

```bash
cd tests
./run_tests.sh
```

Tests include:
- Kernel invariant violation tests
- Payment disabled enforcement tests
- Authentication tests
- Offline manager tests

## Important Notes

### Payments Are Disabled

All payment functionality is disabled. See `PAYMENT_POLICY.md` for requirements before enabling.

### Security Limitations

- No encryption at rest
- Secrets should use environment variables
- See `SECURITY_MODEL.md` for details

### Admin Access

Default admin credentials are in the auth module. **Change these before production use.**

## License

Proprietary - NTRLI Organization

## Contributing

1. Read `ARCHITECTURE.md` and `SECURITY_MODEL.md`
2. Run tests before submitting changes
3. Do not enable payments without completing all requirements
