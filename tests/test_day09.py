import pytest

from solutions.day09 import predict_next_value, predict_previous_value
from tests.utils import assert_solution_part_returns_expected


@pytest.mark.parametrize(
    ("history", "next_value"),
    [
        ([0, 3, 6, 9, 12, 15], 18),
        ([1, 3, 6, 10, 15, 21], 28),
        ([10, 13, 16, 21, 30, 45], 68),
    ],
)
def test_predict_next_value(history: list[int], next_value: int) -> None:
    assert predict_next_value(history) == next_value


@pytest.mark.parametrize(
    ("history", "previous_value"),
    [
        ([0, 3, 6, 9, 12, 15], -3),
        ([1, 3, 6, 10, 15, 21], 0),
        ([10, 13, 16, 21, 30, 45], 5),
    ],
)
def test_predict_previous_value(history: list[int], previous_value: int) -> None:
    assert predict_previous_value(history) == previous_value


def test_part_1() -> None:
    assert_solution_part_returns_expected(9, 1, 1681758908)


def test_part_2() -> None:
    assert_solution_part_returns_expected(9, 2, 803)
