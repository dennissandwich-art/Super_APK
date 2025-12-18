#!/bin/bash
# Run all unit tests

echo "====================================="
echo "Super_APK Test Suite"
echo "====================================="
echo ""

# Run each test file
python3 test_auth.py
python3 test_payment.py

echo ""
echo "====================================="
echo "Test Suite Complete"
echo "====================================="
