# SUPER_APK — MINIMUM BUILD SPECIFICATION

## Status: VERIFIED ✓

---

## 1. MINIMUM RUNTIME COMPONENTS

These files are REQUIRED for the app to build and run:

### Core
| File | Role |
|------|------|
| `main.py` | Entrypoint |
| `app_kernel.py` | Core kernel |
| `lifecycle_hooks.py` | Android lifecycle |

### Events
| File | Role |
|------|------|
| `kernel_events.py` | Event bus integration |
| `kernel_ready.py` | Ready signal |
| `ui_events.py` | UI event bindings |
| `event_bus.py` | Event bus core |

### UI
| File | Role |
|------|------|
| `ui_router.py` | Screen routing |
| `ui_login.py` | Login screen |
| `ui_login_result.py` | Result screen |

### Auth
| File | Role |
|------|------|
| `telegram_login_handler.py` | Login flow |
| `auth_client.py` | Backend HTTP client |
| `session_storage.py` | Token storage |

### Support
| File | Role |
|------|------|
| `kernel_state.py` | State management |
| `error_boundary.py` | Error handling |
| `safe_logger.py` | Logging |
| `kernel_boot.py` | Boot sequence |
| `feature_flags.py` | Feature flags |
| `kernel_features.py` | Feature system |

---

## 2. NOT IN RUNTIME (Contract Only)

These exist but are NOT loaded at runtime:

| Directory | Purpose |
|-----------|---------|
| `assistant/` | AI assistant (future feature) |
| `backend/` | Server code (separate deployment) |
| `analysis/` | Analysis scripts (offline) |
| `legacy/` | Old code (archived) |

---

## 3. BUILD RULES

### MUST be true:
- [ ] App starts without network
- [ ] App starts without permissions
- [ ] Login screen renders first
- [ ] No AI at startup
- [ ] No Stripe at startup

### MUST NOT happen:
- [ ] Import from `legacy/`
- [ ] Import from `assistant/` in main.py
- [ ] Network call before user action
- [ ] Permission request before login

---

## 4. VERIFICATION

Run before building:

```bash
python verify_build.py
```

Expected output:
```
✓ BUILD VERIFICATION PASSED
  Ready for buildozer
```

---

## 5. BUILD COMMAND

```bash
buildozer android debug
```

---

## 6. AFTER BUILD

Test checklist:
1. App installs
2. App starts
3. Login screen visible
4. "Login med Telegram" button works
5. Backend failure shows "Login utilgængeligt"
6. App doesn't crash

---

## 7. AI ASSISTANT ACTIVATION (LATER)

AI assistant is designed but NOT active.

To activate (after login is stable):
1. Create `feature/ai-assistant` branch
2. Add import to main.py
3. Gate behind feature flag
4. Test in isolation
5. Merge only if stable

---

*Last verified: Build verification script passed*
