# kernel_health.py
# BRANCH: main
# ROLE: Kernel health snapshot (READ-ONLY)

class KernelHealth:
    def __init__(self, kernel):
        self.initialized = kernel.state.initialized
        self.features = kernel.features.dump() if kernel.features else {}
        self.errors = kernel.errors.get_errors()

    def ok(self) -> bool:
        return self.initialized and not self.errors
