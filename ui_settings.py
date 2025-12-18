# ui_settings.py
# BRANCH: main
# ROLE: UI-facing settings interface

from settings_store import SettingsStore


class UISettings:
    def __init__(self):
        self.store = SettingsStore()

    def enable_feature(self, name: str):
        self.store.set(name, True)

    def disable_feature(self, name: str):
        self.store.set(name, False)

    def is_enabled(self, name: str) -> bool:
        return bool(self.store.get(name, False))
