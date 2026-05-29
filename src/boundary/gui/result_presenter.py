"""Format boundary facade outcomes for GUI display."""

from __future__ import annotations

from boundary.models.validation_failure_result import ValidationFailureResult

NOT_IMPLEMENTED_MESSAGE: str = (
    "입력 형식은 올바릅니다. 풀이 기능은 아직 구현 중입니다."
)
UNEXPECTED_ERROR_MESSAGE: str = "예기치 않은 오류가 발생했습니다. 다시 시도해 주세요."


def format_validation_failure(result: ValidationFailureResult) -> str:
    """Render a boundary validation failure for the result panel."""
    return f"[{result.code}] {result.message}"


def format_solver_success(payload: list[int]) -> str:
    """Render a six-element solver payload for the result panel."""
    if len(payload) != 6:
        return f"풀이 결과 형식이 올바르지 않습니다. (길이 {len(payload)})"
    r1, c1, n1, r2, c2, n2 = payload
    return (
        "풀이 성공\n"
        f"  빈칸 1: 행 {r1}, 열 {c1} → {n1}\n"
        f"  빈칸 2: 행 {r2}, 열 {c2} → {n2}"
    )


def format_facade_result(result: object) -> str:
    """Map a facade return value to user-facing text."""
    if isinstance(result, ValidationFailureResult) and result.is_failure:
        return format_validation_failure(result)
    if isinstance(result, list):
        return format_solver_success(result)
    return "처리가 완료되었습니다."
