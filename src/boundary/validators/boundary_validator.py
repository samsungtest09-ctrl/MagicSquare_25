"""FR-01 input shape and null validation (AC-FR-01-01 skeleton)."""

from __future__ import annotations

from boundary.constants import (
    GRID_SIZE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)
from boundary.models.validation_failure_result import ValidationFailureResult


class BoundaryValidator:
    """Validates grid shape before control/entity work runs."""

    def validate(self, grid: list[list[int]] | None) -> ValidationFailureResult:
        """Return a failure result when the grid is null or not 4×4."""
        if self._has_invalid_shape(grid):
            return ValidationFailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
                is_failure=True,
                is_success=False,
            )
        raise NotImplementedError(
            "Valid 4×4 grid handling is out of AC-FR-01-01 skeleton scope."
        )

    def _has_invalid_shape(self, grid: list[list[int]] | None) -> bool:
        if grid is None:
            return True
        if len(grid) != GRID_SIZE:
            return True
        return any(len(row) != GRID_SIZE for row in grid)
