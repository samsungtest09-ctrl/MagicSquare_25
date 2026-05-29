"""Boundary entry facade — validates input before invoking control."""

from __future__ import annotations

from boundary.models.validation_failure_result import ValidationFailureResult
from boundary.validators.boundary_validator import BoundaryValidator
from control.use_cases.solver import Solver


def validate_and_solve(
    grid: list[list[int]] | None,
) -> ValidationFailureResult:
    """Run boundary validation; call control only when shape checks pass."""
    validation = BoundaryValidator().validate(grid)
    if validation.is_failure:
        return validation
    return Solver().resolve(grid)
