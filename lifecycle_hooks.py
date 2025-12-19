# lifecycle_hooks.py
# BRANCH: main
# ROLE: Android lifecycle hooks (SAFE, NO SIDE-EFFECTS)

"""
LIFECYCLE HOOKS:
- on_pause: App goes to background
- on_resume: App returns to foreground
- on_stop: App is closing

All hooks are no-op by default.
No state modification at import time.
"""


class LifecycleHooks:
    def __init__(self):
        self._paused = False
        self._stopped = False

    def on_pause(self):
        """Called when app goes to background."""
        self._paused = True

    def on_resume(self):
        """Called when app returns to foreground."""
        self._paused = False

    def on_stop(self):
        """Called when app is closing."""
        self._stopped = True

    def is_paused(self) -> bool:
        return self._paused

    def is_stopped(self) -> bool:
        return self._stopped
