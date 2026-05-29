"""Generate tests/golden_master_expected.txt from current solver capture output."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = PROJECT_ROOT / "tests"
sys.path.insert(0, str(TESTS_DIR))

from golden_master.approve import DEFAULT_EXPECTED_PATH, approve_golden_master


def main() -> int:
    """Write the Golden Master baseline file using the approve bootstrap path."""
    approved = approve_golden_master(DEFAULT_EXPECTED_PATH, auto_approve=True)
    print(f"Wrote Golden Master baseline: {DEFAULT_EXPECTED_PATH}")
    print(approved)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
