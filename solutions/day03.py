from collections.abc import Iterator

from solutions.base import BaseSolution
from solutions.utilities.grid import Coordinate, generate_neighbours, input_to_char_grid


def get_full_number_from_position_in_line(
    line: list[str], position: int
) -> tuple[int, list[int]]:
    """Get the full number at a position in a line

    :param line: The line
    :param position: The position in the line
    :return: The number at the position
    """
    start = position
    for i in range(position - 1, -1, -1):
        if not line[i].isdigit():
            break
        start = i

    end = position
    for i in range(position + 1, len(line)):
        if not line[i].isdigit():
            break
        end = i

    return int("".join(line[start : end + 1])), list(range(start, end + 1))


def generate_symbol_positions(grid: list[list[str]]) -> Iterator[Coordinate]:
    """Generate the positions of symbols in a grid

    :param grid: The grid
    :return: The positions of symbols in the grid
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "." or grid[i][j].isdigit():
                continue
            yield i, j


class Solution(BaseSolution):
    def check_neighbours(
        self, pos: Coordinate, checked_digits: set[Coordinate], numbers: list[int]
    ) -> None:
        for m, n in generate_neighbours(pos, diagonal=True):
            if self.input[m][n].isdigit():
                if (m, n) in checked_digits:
                    continue
                number, found_positions = get_full_number_from_position_in_line(
                    self.input[m], n
                )
                numbers.append(number)
                checked_digits.update((m, p) for p in found_positions)

    def setup(self) -> None:
        self.input = input_to_char_grid(self.raw_input)

    def part_1(self) -> int:
        checked_digits: set[Coordinate] = set()
        numbers: list[int] = []
        for pos in generate_symbol_positions(self.input):
            self.check_neighbours(pos, checked_digits, numbers)
        return sum(numbers)

    def part_2(self) -> int:
        gear_ratios = []
        for i, j in generate_symbol_positions(self.input):
            if self.input[i][j] == "*":
                checked_digits: set[Coordinate] = set()
                numbers: list[int] = []
                self.check_neighbours((i, j), checked_digits, numbers)
                if len(numbers) == 2:  # Only 2 numbers in a gear ratio
                    gear_ratios.append(numbers[0] * numbers[1])
        return sum(gear_ratios)
