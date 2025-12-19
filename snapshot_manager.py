# snapshot_manager.py
# BRANCH: main
# ROLE: Snapshot manager (MEMORY-ONLY)

class SnapshotManager:
    def __init__(self):
        self._snapshots = {}

    def save(self, name: str, data: dict):
        self._snapshots[name] = dict(data)

    def load(self, name: str) -> dict:
        return dict(self._snapshots.get(name, {}))

    def list(self):
        return list(self._snapshots.keys())
