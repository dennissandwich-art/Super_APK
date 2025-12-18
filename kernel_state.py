# kernel_state.py
# BRANCH: main
# ROLE: Deterministic kernel state container

"""
This module defines a plain state object.
It is safe to serialize, log, or reset.
"""

class KernelState:
    def __init__(self):
        self.initialized = False
        self.features_enabled = {}
        self.errors = []

    def mark_initialized(self):
        self.initialized = True

    def enable_feature(self, name: str):
        self.features_enabled[name] = True

    def disable_feature(self, name: str):
        self.features_enabled[name] = False

    def add_error(self, message: str):
        self.errors.append(message)
