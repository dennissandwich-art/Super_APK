"""
Unit tests for authentication module
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import AuthManager

class TestAuthManager(unittest.TestCase):
    """Test cases for AuthManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.auth = AuthManager()

    def test_admin_user_exists(self):
        """Test that admin user is created automatically"""
        self.assertIn("Sir_NTRLI_II", self.auth.users)

    def test_admin_user_role(self):
        """Test that admin user has correct role"""
        admin_user = self.auth.users.get("Sir_NTRLI_II")
        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user["role"], "admin")

    def test_user_registration(self):
        """Test user registration"""
        success, msg = self.auth.register_user("testuser", "testpass123")
        self.assertTrue(success)
        self.assertIn("testuser", self.auth.users)

    def test_duplicate_registration(self):
        """Test that duplicate registration fails"""
        self.auth.register_user("testuser2", "testpass123")
        success, msg = self.auth.register_user("testuser2", "differentpass")
        self.assertFalse(success)

    def test_successful_login(self):
        """Test successful login"""
        success, token, msg = self.auth.login("Sir_NTRLI_II", "NTRLI_ADMIN_2024")
        self.assertTrue(success)
        self.assertIsNotNone(token)

    def test_failed_login_invalid_password(self):
        """Test failed login with invalid password"""
        success, token, msg = self.auth.login("Sir_NTRLI_II", "wrongpassword")
        self.assertFalse(success)
        self.assertIsNone(token)

    def test_failed_login_invalid_user(self):
        """Test failed login with invalid user"""
        success, token, msg = self.auth.login("nonexistentuser", "password")
        self.assertFalse(success)
        self.assertIsNone(token)

    def test_session_validation(self):
        """Test session token validation"""
        success, token, msg = self.auth.login("Sir_NTRLI_II", "NTRLI_ADMIN_2024")
        self.assertTrue(success)

        valid, session = self.auth.validate_session(token)
        self.assertTrue(valid)
        self.assertEqual(session["username"], "Sir_NTRLI_II")

    def test_invalid_session_validation(self):
        """Test invalid session token validation"""
        valid, session = self.auth.validate_session("invalid_token")
        self.assertFalse(valid)

    def test_admin_check(self):
        """Test admin role checking"""
        success, token, msg = self.auth.login("Sir_NTRLI_II", "NTRLI_ADMIN_2024")
        self.assertTrue(success)

        is_admin = self.auth.is_admin(token)
        self.assertTrue(is_admin)

    def test_logout(self):
        """Test logout functionality"""
        success, token, msg = self.auth.login("Sir_NTRLI_II", "NTRLI_ADMIN_2024")
        self.assertTrue(success)

        logout_success = self.auth.logout(token)
        self.assertTrue(logout_success)

        # Session should be invalid after logout
        valid, session = self.auth.validate_session(token)
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()
