"""Entity-track fixtures — Report/09 G0~G3 placeholders (RED skeleton)."""

from __future__ import annotations

# G0 — complete magic square (no blanks)
# [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]

# G1 — D-LOC-01 / D-MIS-01 / D-SOL-01 anchor; blanks at (2,2),(3,3) 1-index
# [[16, 3, 2, 13], [5, 0, 11, 8], [9, 6, 0, 12], [4, 15, 14, 1]]

# G2 — D-SOL-02 Step B reverse (PRD TD-002); fixture TBD in GREEN
# [[0, 14, 15, 4], [9, 7, 6, 12], [5, 11, 10, 8], [16, 2, 3, 13]]

# G3 — D-SOL-03 both attempts fail (PRD TD-007)
# [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 12], [13, 14, 15, 0]]

# @pytest.fixture
# def grid_g0() -> list[list[int]]:
#     ...

# @pytest.fixture
# def grid_g1() -> list[list[int]]:
#     ...

# @pytest.fixture
# def grid_g2() -> list[list[int]]:
#     ...

# @pytest.fixture
# def grid_g3() -> list[list[int]]:
#     ...
