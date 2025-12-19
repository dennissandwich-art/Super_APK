# feature_toggle_command.py
# BRANCH: main
# ROLE: Toggle feature flags safely (COMMAND)

class FeatureToggleCommand:
    def __init__(self, store, feature_name: str, enabled: bool):
        self.store = store
        self.feature_name = feature_name
        self.enabled = enabled

    def execute(self):
        self.store.set(self.feature_name, self.enabled)
