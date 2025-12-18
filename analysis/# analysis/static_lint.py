# analysis/static_lint.py
# BRANCH: claude-analyze-super-apk
# ROLE: Simple static lint (NO DEPENDENCIES)

"""
Scans for forbidden patterns across repo.
Safe to run on phone.
"""

from pathlib import Path

FORBIDDEN = [
    "import stripe",
    "requests.get(",
    "urllib.request",
]

ROOT = Path(__file__).resolve().parents[1]


def run():
    violations = []
    for path in ROOT.rglob("*.py"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for pattern in FORBIDDEN:
            if pattern in text:
                violations.append((str(path), pattern))

    if violations:
        print("❌ STATIC LINT FAILED")
        for file, pat in violations:
            print("-", file, "contains", pat)
    else:
        print("✅ STATIC LINT PASSED")


if __name__ == "__main__":
    run()
