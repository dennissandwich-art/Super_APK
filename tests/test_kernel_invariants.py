"""
Kernel Invariant Tests
======================

These tests verify that invariant violations CRASH as expected.
A passing test suite means the enforcement is working correctly.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_kernel import (
    AppKernel,
    KernelInvariantViolation,
    SubsystemNotInitializedError,
    get_kernel,
)


class TestKernelSingleton(unittest.TestCase):
    """Test kernel singleton enforcement."""

    def setUp(self):
        """Reset kernel state before each test."""
        AppKernel.reset_for_testing()

    def tearDown(self):
        """Clean up after each test."""
        AppKernel.reset_for_testing()

    def test_single_kernel_allowed(self):
        """Test that one kernel instance can be created."""
        kernel = AppKernel()
        self.assertIsNotNone(kernel)

    def test_second_kernel_crashes(self):
        """Test that creating a second kernel raises KernelInvariantViolation."""
        kernel1 = AppKernel()

        with self.assertRaises(KernelInvariantViolation) as context:
            kernel2 = AppKernel()

        self.assertIn("second AppKernel instance", str(context.exception))

    def test_get_instance_before_init_crashes(self):
        """Test that get_instance() before initialization raises."""
        with self.assertRaises(KernelInvariantViolation) as context:
            get_kernel()

        self.assertIn("Kernel not initialized", str(context.exception))

    def test_get_instance_after_init_works(self):
        """Test that get_instance() works after initialization."""
        kernel = AppKernel()
        retrieved = get_kernel()
        self.assertIs(kernel, retrieved)


class TestSubsystemAccess(unittest.TestCase):
    """Test subsystem access enforcement."""

    def setUp(self):
        """Set up kernel for testing."""
        AppKernel.reset_for_testing()
        self.kernel = AppKernel()

    def tearDown(self):
        """Clean up."""
        AppKernel.reset_for_testing()

    def test_uninitialized_subsystem_crashes(self):
        """Test that accessing uninitialized subsystem raises."""
        # Don't boot kernel - subsystems not initialized
        with self.assertRaises(SubsystemNotInitializedError) as context:
            self.kernel.get_subsystem("nonexistent")

        self.assertIn("not initialized", str(context.exception))

    def test_is_subsystem_available_returns_false_before_boot(self):
        """Test subsystem availability check before boot."""
        self.assertFalse(self.kernel.is_subsystem_available("state"))
        self.assertFalse(self.kernel.is_subsystem_available("network"))


class TestInvariantAssertion(unittest.TestCase):
    """Test invariant assertion mechanism."""

    def setUp(self):
        """Set up kernel for testing."""
        AppKernel.reset_for_testing()
        self.kernel = AppKernel()

    def tearDown(self):
        """Clean up."""
        AppKernel.reset_for_testing()

    def test_assert_invariant_passes_on_true(self):
        """Test that assert_invariant passes on true condition."""
        # Should not raise
        self.kernel.assert_invariant(True, "This should pass")

    def test_assert_invariant_crashes_on_false(self):
        """Test that assert_invariant crashes on false condition."""
        with self.assertRaises(KernelInvariantViolation) as context:
            self.kernel.assert_invariant(False, "Test violation message")

        self.assertIn("INVARIANT VIOLATION", str(context.exception))
        self.assertIn("Test violation message", str(context.exception))

    def test_assert_booted_crashes_before_boot(self):
        """Test that assert_booted crashes if kernel not booted."""
        with self.assertRaises(KernelInvariantViolation) as context:
            self.kernel.assert_booted()

        self.assertIn("Kernel must be booted", str(context.exception))


class TestHealthSnapshot(unittest.TestCase):
    """Test kernel health diagnostics."""

    def setUp(self):
        """Set up kernel for testing."""
        AppKernel.reset_for_testing()
        self.kernel = AppKernel()

    def tearDown(self):
        """Clean up."""
        AppKernel.reset_for_testing()

    def test_health_snapshot_before_boot(self):
        """Test health snapshot before boot."""
        snapshot = self.kernel.health_snapshot()

        self.assertFalse(snapshot["booted"])
        self.assertEqual(snapshot["error_count"], 0)
        self.assertIsNone(snapshot["last_error"])

    def test_error_tracking(self):
        """Test that errors are tracked correctly."""
        self.kernel.report_error("test_component", Exception("Test error"))

        snapshot = self.kernel.health_snapshot()
        self.assertEqual(snapshot["error_count"], 1)
        self.assertIn("test_component", snapshot["last_error"])


class TestShutdownHooks(unittest.TestCase):
    """Test shutdown hook mechanism."""

    def setUp(self):
        """Set up kernel for testing."""
        AppKernel.reset_for_testing()
        self.kernel = AppKernel()
        self.hook_called = False

    def tearDown(self):
        """Clean up."""
        AppKernel.reset_for_testing()

    def test_shutdown_hook_called(self):
        """Test that registered shutdown hooks are called."""
        def my_hook():
            self.hook_called = True

        self.kernel.register_shutdown_hook(my_hook)
        self.kernel.shutdown()

        self.assertTrue(self.hook_called)

    def test_shutdown_hooks_called_in_reverse_order(self):
        """Test that shutdown hooks are called in reverse order."""
        call_order = []

        def hook1():
            call_order.append(1)

        def hook2():
            call_order.append(2)

        def hook3():
            call_order.append(3)

        self.kernel.register_shutdown_hook(hook1)
        self.kernel.register_shutdown_hook(hook2)
        self.kernel.register_shutdown_hook(hook3)
        self.kernel.shutdown()

        self.assertEqual(call_order, [3, 2, 1])


if __name__ == "__main__":
    unittest.main()
