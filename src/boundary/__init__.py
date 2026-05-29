"""Boundary layer — external I/O adapters and input validation."""

from boundary.facade import validate_and_solve
from boundary.validators.boundary_validator import BoundaryValidator

__all__ = ["BoundaryValidator", "validate_and_solve"]
