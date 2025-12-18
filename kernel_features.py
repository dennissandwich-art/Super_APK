# kernel_features.py
# BRANCH: main
# ROLE: Immutable snapshot of enabled features

class KernelFeatures:
    def __init__(self, flags: dict):
        self._flags = dict(flags)

    def enabled(self, name: str) -> bool:
        return self._flags.get(name, False)

    def dump(self):
        return dict(self._flags)
