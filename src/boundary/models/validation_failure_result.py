"""Failure result DTO for boundary validation (AC-FR-01-01)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from boundary.constants import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


class ValidationFailureResult(BaseModel):
    """Typed failure payload returned when FR-01 shape/null checks fail."""

    code: str = Field(default=INVALID_SIZE_CODE)
    message: str = Field(default=INVALID_SIZE_MESSAGE)
    is_failure: bool = Field(default=True)
    is_success: bool = Field(default=False)
