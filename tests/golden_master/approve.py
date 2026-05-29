"""Approval-pattern comparison for Golden Master regression tests."""

from __future__ import annotations

import difflib
import os
import re
from pathlib import Path

from golden_master.capture import capture_all_scenarios, capture_scenario
from golden_master.scenarios import SCENARIOS, Scenario

DEFAULT_EXPECTED_PATH = Path(__file__).resolve().parents[1] / "golden_master_expected.txt"
APPROVE_ENV_VAR = "GOLDEN_MASTER_APPROVE"
_BLOCK_HEADER_PATTERN = re.compile(r"^\[(GM-TC-\d{2})\]", re.MULTILINE)


def _normalize_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def should_auto_approve(auto_approve: bool | None = None) -> bool:
    """Return whether the approve bootstrap path is active."""
    if auto_approve is not None:
        return auto_approve
    return os.environ.get(APPROVE_ENV_VAR, "").strip() == "1"


def format_unified_diff(expected: str, actual: str) -> str:
    """Render a unified diff with expected/actual file labels."""
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )


def extract_scenario_block(expected_text: str, tc_id: str) -> str | None:
    """Extract one scenario block from the baseline file body."""
    normalized = _normalize_text(expected_text)
    headers = list(_BLOCK_HEADER_PATTERN.finditer(normalized))
    for index, match in enumerate(headers):
        if match.group(1) != tc_id:
            continue
        start = match.start()
        end = headers[index + 1].start() if index + 1 < len(headers) else len(normalized)
        return normalized[start:end].rstrip() + "\n"
    return None


def approve_text(
    actual: str,
    expected_path: Path,
    *,
    auto_approve: bool | None = None,
) -> str:
    """Compare actual text with a baseline file using the approve pattern."""
    target_path = expected_path
    actual_normalized = _normalize_text(actual)

    if not target_path.exists() or should_auto_approve(auto_approve):
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(actual_normalized, encoding="utf-8")
        return actual_normalized

    expected_normalized = _normalize_text(target_path.read_text(encoding="utf-8"))
    if actual_normalized == expected_normalized:
        return expected_normalized

    diff = format_unified_diff(expected_normalized, actual_normalized)
    message = (
        "Golden Master mismatch. Set GOLDEN_MASTER_APPROVE=1 to refresh baseline.\n"
        f"{diff}"
    )
    raise AssertionError(message)


def approve_golden_master(
    expected_path: Path | None = None,
    *,
    auto_approve: bool | None = None,
) -> str:
    """Compare all captured scenarios against the stored baseline file."""
    target_path = expected_path or DEFAULT_EXPECTED_PATH
    actual = capture_all_scenarios()
    return approve_text(actual, target_path, auto_approve=auto_approve)


def approve_scenario(
    scenario: Scenario,
    expected_path: Path | None = None,
    *,
    auto_approve: bool | None = None,
) -> str:
    """Compare one scenario block against the stored baseline file."""
    target_path = expected_path or DEFAULT_EXPECTED_PATH
    actual_block = _normalize_text(capture_scenario(scenario))

    if not target_path.exists() or should_auto_approve(auto_approve):
        approve_golden_master(target_path, auto_approve=True)
        return actual_block

    expected_text = target_path.read_text(encoding="utf-8")
    expected_block = extract_scenario_block(expected_text, scenario.tc_id)
    if expected_block is None:
        approve_golden_master(target_path, auto_approve=True)
        return actual_block

    expected_block = _normalize_text(expected_block)
    if actual_block == expected_block:
        return expected_block

    diff = format_unified_diff(expected_block, actual_block)
    message = (
        f"{scenario.tc_id} Golden Master mismatch. "
        f"Set {APPROVE_ENV_VAR}=1 to refresh baseline.\n"
        f"{diff}"
    )
    raise AssertionError(message)
