# analysis/dependency_surface.py
# BRANCH: claude-analyze-super-apk
# ROLE: Dependency surface map

SURFACE = {
    "stdlib_only": True,
    "third_party_at_start": False,
}

def run():
    print("DEPENDENCY SURFACE")
    for k, v in SURFACE.items():
        print("✔", k, "=", v)

if __name__ == "__main__":
    run()
