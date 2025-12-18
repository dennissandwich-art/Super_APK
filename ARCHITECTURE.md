# Super_APK Architecture

## Overview

Super_APK is an Android application built with Kivy/KivyMD. This document describes the actual architecture as implemented.

## Taxonomy Levels

### 1. Conceptual Level
- **AppKernel**: Single execution authority for the application
- **StateManager**: Centralized state management (Redux-style)
- **Subsystems**: Network, Storage, Monitoring

### 2. Logical Level
- Dependency injection via kernel
- Singleton enforcement for kernel
- Event-driven state updates

### 3. Physical Level
- Python 3 codebase
- Kivy/KivyMD UI framework
- JSON file-based persistence

### 4. Operational Level
- Unit tests in `tests/`
- Invariant violation tests
- CI via GitHub Actions (planned)

## Core Components

### AppKernel (`app_kernel.py`)

The kernel is the **single execution authority**. It:
- Enforces singleton pattern (only one instance allowed)
- Initializes all subsystems in correct order
- Provides dependency injection
- Owns application lifecycle
- **Crashes on invariant violations**

```python
# Correct usage
kernel = AppKernel()
kernel.boot()

# This WILL crash (second instance)
kernel2 = AppKernel()  # KernelInvariantViolation
```

### StateManager (`state_manager.py`)

Redux-style centralized state management:
- Single source of truth
- Immutable state updates via dispatch
- Subscriber pattern for reactivity
- Time-travel debugging support

```python
state = AppState()
state.dispatch({"type": "USER_LOGIN", "payload": {...}})
```

### SecureStorage (`secure_storage.py`)

Storage for application data:
- File-based with filesystem permissions
- Uses `python-keyring` for secrets when available
- **Does NOT implement custom cryptography**
- **Not suitable for API keys** (use env vars)

## Module Dependencies

```
main.py
  └── app_kernel.py (kernel)
        ├── state_manager.py
        ├── network.py
        ├── monitoring.py
        └── (other subsystems)
```

## What Is NOT Implemented

- **Payment processing** - Disabled, see `sandbox/stripe-experiment/`
- **Push notifications** - Not implemented
- **Background sync** - Partial, via OfflineManager
- **Encryption at rest** - Not implemented (uses OS permissions)

## Testing

Run tests:
```bash
cd tests
./run_tests.sh
```

Key test categories:
- Invariant violation tests (kernel crashes correctly)
- Payment disabled tests (security enforcement)
- Auth tests
- Offline manager tests
