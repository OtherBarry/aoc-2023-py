from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solutions.base import BaseSolution


def assert_solution_part_returns_expected(
    problem: int, part: int, expected: int
) -> None:
    """Assert that the solution part returns the expected value

    :param solution_id: The solution ID
    :param part: The part of the solution
    :param expected: The expected value
    """
    input_path = Path(f"inputs/{problem:02d}.txt")
    solution_class: type[BaseSolution] = import_module(
        f"solutions.day{problem:02d}"
    ).Solution
    solution = solution_class(input_path)
    solution.setup()
    if part == 1:
        assert solution.part_1() == expected  # noqa: S101
    elif part == 2:
        assert solution.part_2() == expected  # noqa: S101
    else:
        msg = f"Invalid part: {part}"
        raise ValueError(msg)
