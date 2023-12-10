import pytest

from solutions.day01 import Solution
from tests.utils import assert_solution_part_returns_expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [("1abc2", 12), ("pqr3stu8vwx", 38), ("a1b2c3d4e5f", 15), ("treb7uchet", 77)],
)
def test_extract_digits(line: str, expected: int) -> None:
    assert Solution.calculate_calibration_value(line, include_words=False) == expected


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
        # additional test case
        ("trknlxnv43zxlrqjtwonect", 41),
    ],
)
def test_extract_digits_including_digits_as_words(line: str, expected: int) -> None:
    assert Solution.calculate_calibration_value(line, include_words=True) == expected


def test_part_1() -> None:
    assert_solution_part_returns_expected(1, 1, 56049)


def test_part_2() -> None:
    assert_solution_part_returns_expected(1, 2, 54530)
