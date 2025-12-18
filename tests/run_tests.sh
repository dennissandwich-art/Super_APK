#!/bin/bash
# Run all unit tests for Super_APK

set -e  # Exit on first failure

echo "====================================="
echo "Super_APK Test Suite"
echo "====================================="
echo ""

cd "$(dirname "$0")"

# Track failures
FAILED=0

run_test() {
    echo "Running: $1"
    if python3 "$1" -v 2>&1; then
        echo "PASSED: $1"
    else
        echo "FAILED: $1"
        FAILED=$((FAILED + 1))
    fi
    echo ""
}

# Core invariant tests (these MUST pass)
echo "=== INVARIANT TESTS (must crash on violation) ==="
run_test test_kernel_invariants.py

# Payment disabled tests (security enforcement)
echo "=== SECURITY ENFORCEMENT TESTS ==="
run_test test_payment_disabled.py

# Offline manager tests
echo "=== OFFLINE MANAGER TESTS ==="
run_test test_offline_manager.py

# Auth tests
echo "=== AUTH TESTS ==="
run_test test_auth.py

echo "====================================="
if [ $FAILED -eq 0 ]; then
    echo "ALL TESTS PASSED"
    exit 0
else
    echo "FAILED: $FAILED test file(s)"
    exit 1
fi
