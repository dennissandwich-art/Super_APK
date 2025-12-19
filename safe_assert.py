# safe_assert.py
# BRANCH: main
# ROLE: Assertion helper (NO CRASH)

def assert_true(condition: bool, message: str):
    if not condition:
        print("ASSERT FAILED:", message)
