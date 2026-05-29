# Golden Master Approve Pattern — GM-1 / GM-2 Design

| 항목 | 내용 |
|---|---|
| **문서 ID** | GM-MS-APPROVE-02 |
| **대상** | Magic Square Solver 출력 회귀 테스트 |
| **기준 파일** | `tests/golden_master_expected.txt` |
| **생성 스크립트** | `scripts/generate_golden_master.py` |
| **테스트** | `tests/test_golden_master_magic_square.py` |
| **마커** | `@pytest.mark.golden_master` / `[TAG][GoldenMaster]` |
| **작성일** | 2026-05-29 |

---

## 1. 목적

Magic Square Solver의 **실제 캡처 출력**을 버전 관리되는 Golden Master 기준 파일과 비교하여, 리팩토링·GREEN 구현 이후에도 입출력 계약이 깨지지 않도록 회귀를 방지한다.

---

## 2. 캡처 전략

### 2.1 입력 시나리오 (GM-TC SSOT)

| 시나리오 ID | 의미 | name |
|---|---|---|
| `GM-TC-01` | small-first 조합 성공 | `normal_success` |
| `GM-TC-02` | reverse 조합 성공 | `reverse_success` |
| `GM-TC-03` | 빈칸 개수 ≠ 2 | `invalid_blank_count` |
| `GM-TC-04` | non-zero 중복 | `duplicate_number` |
| `GM-TC-05` | 양 Attempt 실패 | `no_valid_magic_square` |

시나리오 정의 SSOT: `tests/golden_master/scenarios.py`

### 2.2 출력 캡처

현재 GM-1 단계에서는 **Result DTO 직렬화** 방식을 사용한다.

- 성공: `Output:\n[r1,c1,n1,r2,c2,n2]`
- 실패: `Error:\n<CODE>`

캡처 파이프라인:

```text
Scenario grid
    → reference capture (tests/golden_master/capture.py)
    → serializer (tests/golden_master/serializer.py)
    → scenario block text
```

> **GREEN 이후 전환:** `capture.py`가 `boundary.facade.validate_and_solve()` 결과를 직렬화하도록 교체하면, 동일 approve 패턴으로 프로덕션 출력을 회귀 보호할 수 있다.

---

## 3. 기준 파일 구조

```text
[normal_success]
Input:
16 2 3 13
5 11 10 8
9 7 0 12
4 14 15 0
Output:
[3,3,1,4,4,6]

[reverse_success]
Input:
...
Output:
[1,1,16,1,2,2]

[invalid_blank_count]
Input:
...
Error:
INVALID_BLANK_COUNT

[duplicate_number]
Input:
...
Error:
DUPLICATE_NUMBER

[no_valid_solution]
Input:
...
Error:
NO_VALID_SOLUTION
```

- 시나리오 구분: `[scenario_name]` 헤더
- 입력: `Input:` 다음 4행 공백 구분 정수
- 성공: `Output:` 다음 6원소 배열
- 실패: `Error:` 다음 오류 코드 문자열
- 시나리오 블록 사이: 빈 줄 1개

---

## 4. Approve 패턴

구현: `tests/golden_master/approve.py`

| 조건 | 동작 |
|---|---|
| 기준 파일 **없음** | 현재 캡처 출력으로 자동 생성 |
| `GOLDEN_MASTER_APPROVE=1` | 현재 출력으로 기준 파일 **갱신** |
| 기준 파일 **있음** (기본) | `actual` vs `expected` 문자열 비교 |
| **불일치** | `difflib.unified_diff` 출력 후 `AssertionError` (pytest FAIL) |

### 4.1 기준 파일 최초 생성

```bash
python scripts/generate_golden_master.py
```

또는:

```bash
GOLDEN_MASTER_APPROVE=1 python -m pytest tests/test_golden_master.py -v
```

### 4.2 회귀 검증 (기본)

```bash
pytest -m golden_master -v
```

또는:

```bash
python -m pytest tests/test_golden_master_magic_square.py -v
```

### 4.3 의도적 출력 변경 승인

```bash
# PowerShell
$env:GOLDEN_MASTER_APPROVE=1
python -m pytest tests/test_golden_master.py -v
```

```bash
# bash
GOLDEN_MASTER_APPROVE=1 python -m pytest tests/test_golden_master.py -v
```

---

## 5. 모듈 책임

| 모듈 | 레이어 | 책임 |
|---|---|---|
| `tests/golden_master/scenarios.py` | Test SSOT | GM-1 입력·기대 결과 정의 |
| `tests/golden_master/capture.py` | Test infra | 격자 → 성공/실패 캡처 |
| `tests/golden_master/serializer.py` | Test infra | DTO/결과 → 텍스트 블록 |
| `tests/golden_master/approve.py` | Test infra | approve 비교·diff·bootstrap |
| `scripts/generate_golden_master.py` | Tooling | 기준 파일 생성 CLI |
| `tests/test_golden_master_magic_square.py` | Test | pytest 회귀 진입점 (GM-TC-01~05) |

ECB 경계: Golden Master 유틸은 **tests** 패키지에만 존재하며, `boundary` / `control` / `entity` 운영 코드를 직접 수정하지 않는다.

---

## 6. 버전 관리

- `tests/golden_master_expected.txt`는 **반드시 git에 포함**한다.
- 생성 스크립트 실행 후:

```bash
git add tests/golden_master_expected.txt
```

---

## 7. 실패 시 대응

1. `pytest tests/test_golden_master.py -v` 로 diff 확인
2. 버그 수정이면 구현을 고친다.
3. 계약 변경이 의도된 경우 `GOLDEN_MASTER_APPROVE=1`로 baseline을 갱신하고 PR에 diff를 명시한다.
