"""Serialize solver outcomes into Golden Master text blocks."""

from __future__ import annotations

from golden_master.scenarios import Scenario


def format_grid_input(grid: list[list[int]]) -> str:
    """Render a 4x4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_success_output(payload: list[int]) -> str:
    """Render a six-element solver payload."""
    inner = ",".join(str(value) for value in payload)
    return f"[{inner}]"


def format_error_output(error_code: str) -> str:
    """Render a boundary or domain error code."""
    return error_code


def serialize_scenario_block(
    scenario: Scenario,
    *,
    output: list[int] | None = None,
    error: str | None = None,
) -> str:
    """Serialize one scenario into the GM block format."""
    lines = [
        f"[{scenario.tc_id}]",
        f"Name: {scenario.name}",
        "Input:",
        format_grid_input(scenario.grid),
    ]
    if error is not None:
        lines.extend(["Error:", format_error_output(error)])
    elif output is not None:
        lines.extend(["Output:", format_success_output(output)])
    else:
        msg = "serialize_scenario_block requires output or error"
        raise ValueError(msg)
    return "\n".join(lines)


def serialize_all_scenario_blocks(blocks: list[str]) -> str:
    """Join scenario blocks with a blank line separator."""
    return "\n\n".join(blocks) + "\n"
