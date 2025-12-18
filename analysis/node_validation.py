# analysis/node_validation.py
# BRANCH: claude-analyze-super-apk
# ROLE: Static durability validation (NO RUNTIME EFFECTS)

"""
This script performs STATIC checks only.
It must never be imported by the app.
It is safe to delete after analysis.
"""

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


FORBIDDEN_IMPORTS = {
    "stripe",
    "requests",
    "urllib",
}


ENTRYPOINT_FILES = {
    "main.py",
}


def scan_file_forbidden_imports(file_path: Path):
    violations = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return violations

    for forbidden in FORBIDDEN_IMPORTS:
        if f"import {forbidden}" in content:
            violations.append(forbidden)

    return violations


def validate_entrypoints():
    errors = []

    for entry in ENTRYPOINT_FILES:
        entry_path = ROOT / entry
        if not entry_path.exists():
            errors.append(f"Missing entrypoint: {entry}")
            continue

        violations = scan_file_forbidden_imports(entry_path)
        if violations:
            errors.append(
                f"{entry} contains forbidden imports: {violations}"
            )

    return errors


def main():
    errors = validate_entrypoints()

    if errors:
        print("❌ NODE VALIDATION FAILED")
        for err in errors:
            print(" -", err)
        sys.exit(1)

    print("✅ NODE VALIDATION PASSED")
    print("Main entrypoints are clean and durable.")


if __name__ == "__main__":
    main()
