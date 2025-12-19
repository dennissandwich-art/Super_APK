# verify_build.py
# BRANCH: main
# ROLE: Build verification script (RUN BEFORE BUILD)

"""
BUILD VERIFICATION:
1. Tests all imports resolve
2. Verifies AI is NOT in runtime path
3. Checks for syntax errors
4. Lists minimum components

Run: python verify_build.py
"""

import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')


def mock_kivy():
    """Mock Kivy for import testing."""
    class FakeWidget:
        def __init__(self, **kwargs):
            pass
        def add_widget(self, w):
            pass
        def bind(self, **kwargs):
            pass

    class FakeApp:
        def run(self):
            pass

    mods = {
        'kivy': type(sys)('kivy'),
        'kivy.app': type(sys)('kivy.app'),
        'kivy.uix': type(sys)('kivy.uix'),
        'kivy.uix.boxlayout': type(sys)('kivy.uix.boxlayout'),
        'kivy.uix.button': type(sys)('kivy.uix.button'),
        'kivy.uix.label': type(sys)('kivy.uix.label'),
        'kivy.uix.textinput': type(sys)('kivy.uix.textinput'),
        'kivy.uix.scrollview': type(sys)('kivy.uix.scrollview'),
    }

    mods['kivy.app'].App = FakeApp
    mods['kivy.uix.boxlayout'].BoxLayout = FakeWidget
    mods['kivy.uix.button'].Button = FakeWidget
    mods['kivy.uix.label'].Label = FakeWidget
    mods['kivy.uix.textinput'].TextInput = FakeWidget
    mods['kivy.uix.scrollview'].ScrollView = FakeWidget

    sys.modules.update(mods)


def test_imports():
    """Test all required imports."""
    print("=" * 50)
    print("TESTING IMPORTS")
    print("=" * 50)

    mock_kivy()

    required = [
        ('app_kernel', 'AppKernel'),
        ('lifecycle_hooks', 'LifecycleHooks'),
        ('kernel_events', 'KernelEvents'),
        ('kernel_ready', 'emit_ready'),
        ('ui_router', 'UIRouter'),
        ('ui_events', 'UIEvents'),
        ('ui_login', 'LoginState'),
        ('telegram_login_handler', 'TelegramLoginHandler'),
        ('auth_client', 'AuthClient'),
        ('session_storage', 'SessionStorage'),
    ]

    all_ok = True
    for module, attr in required:
        try:
            mod = __import__(module)
            if hasattr(mod, attr):
                print(f"✓ {module}.{attr}")
            else:
                print(f"✗ {module}.{attr} NOT FOUND")
                all_ok = False
        except Exception as e:
            print(f"✗ {module}: {e}")
            all_ok = False

    return all_ok


def test_no_ai_in_runtime():
    """Verify AI assistant is not in runtime path."""
    print()
    print("=" * 50)
    print("VERIFYING AI NOT IN RUNTIME")
    print("=" * 50)

    # Import main
    from main import SuperAPKApp

    # Check
    ai_loaded = any(
        m.startswith('assistant')
        for m in sys.modules
    )

    if ai_loaded:
        print("✗ AI assistant IS in runtime path")
        return False
    else:
        print("✓ AI assistant is NOT in runtime path")
        return True


def test_no_legacy_imports():
    """Verify legacy files are not imported."""
    print()
    print("=" * 50)
    print("VERIFYING NO LEGACY IMPORTS")
    print("=" * 50)

    legacy = ['admin', 'auth', 'ecommerce', 'network', 'news', 'ai', 'i18n']

    legacy_loaded = [
        m for m in legacy
        if m in sys.modules and 'legacy' not in sys.modules.get(m, '').__file__
    ]

    if legacy_loaded:
        print(f"✗ Legacy modules loaded: {legacy_loaded}")
        return False
    else:
        print("✓ No legacy modules in runtime")
        return True


def list_runtime_components():
    """List minimum runtime components."""
    print()
    print("=" * 50)
    print("MINIMUM RUNTIME COMPONENTS")
    print("=" * 50)

    components = [
        ("main.py", "Entrypoint"),
        ("app_kernel.py", "Core kernel"),
        ("lifecycle_hooks.py", "Android lifecycle"),
        ("kernel_events.py", "Event system"),
        ("kernel_ready.py", "Ready signal"),
        ("ui_router.py", "UI routing"),
        ("ui_events.py", "UI event bindings"),
        ("ui_login.py", "Login screen"),
        ("ui_login_result.py", "Result screen"),
        ("telegram_login_handler.py", "Login flow"),
        ("auth_client.py", "Backend client"),
        ("session_storage.py", "Session storage"),
    ]

    for file, role in components:
        exists = os.path.exists(file)
        status = "✓" if exists else "✗"
        print(f"{status} {file:30} {role}")


def main():
    print()
    print("SUPER_APK BUILD VERIFICATION")
    print("=" * 50)
    print()

    results = []

    results.append(("Imports", test_imports()))
    results.append(("AI isolation", test_no_ai_in_runtime()))
    results.append(("Legacy isolation", test_no_legacy_imports()))

    list_runtime_components()

    print()
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)

    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("✓ BUILD VERIFICATION PASSED")
        print("  Ready for buildozer")
        return 0
    else:
        print("✗ BUILD VERIFICATION FAILED")
        print("  Fix issues before building")
        return 1


if __name__ == "__main__":
    sys.exit(main())
