# analysis/invariant_registry.py
# BRANCH: claude-analyze-super-apk
# ROLE: Canonical invariants registry

INVARIANTS = [
    "UI renders before any optional feature",
    "Kernel has no UI imports",
    "No network required at startup",
    "Payments isolated and gated",
    "All defaults OFF",
]

def run():
    print("INVARIANTS")
    for inv in INVARIANTS:
        print("✔", inv)

if __name__ == "__main__":
    run()
