# analysis/coupling_check.py
# BRANCH: claude-analyze-super-apk
# ROLE: Detect forbidden cross-layer imports

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_RULES = [
    ("main", "payments"),
    ("app_kernel", "kivy"),
]


def run():
    violations = []
    for py in ROOT.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8")
        except Exception:
            continue

        for a, b in FORBIDDEN_RULES:
            if a in text and b in text:
                violations.append(str(py))

    if violations:
        print("❌ COUPLING VIOLATIONS")
        for v in violations:
            print("-", v)
    else:
        print("✅ NO COUPLING VIOLATIONS")


if __name__ == "__main__":
    run()
