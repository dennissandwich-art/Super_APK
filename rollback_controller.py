# rollback_controller.py
# BRANCH: main
# ROLE: Rollback controller (DETERMINISTIC)

from snapshot_manager import SnapshotManager

class RollbackController:
    def __init__(self):
        self.snapshots = SnapshotManager()

    def checkpoint(self, name: str, state: dict):
        self.snapshots.save(name, state)

    def rollback(self, name: str) -> dict:
        return self.snapshots.load(name)
