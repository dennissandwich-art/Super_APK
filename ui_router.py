# ui_router.py
# BRANCH: main
# ROLE: Deterministic UI routing (SAFE)

from ui_boot import BootScreen


class UIRouter:
    def __init__(self):
        self.current = None

    def route_initial(self):
        self.current = BootScreen()
        return self.current
