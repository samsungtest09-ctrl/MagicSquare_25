"""Control layer solver orchestration (skeleton)."""

from __future__ import annotations


class Solver:
    """Domain resolution entry point; invoked only after boundary validation passes."""

    def resolve(self, grid: list[list[int]]) -> None:
        """Resolve blanks into a magic square candidate (not implemented)."""
        raise NotImplementedError("Solver.resolve is not implemented yet.")
