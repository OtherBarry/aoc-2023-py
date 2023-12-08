from collections.abc import Generator

from solutions.base import BaseSolution


def generate_neighbours(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    """Generate the neighbours of a coordinate

    :param x: The x coordinate
    :param y: The y coordinate
    :return: The neighbours of the coordinate
    """
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


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


def generate_symbol_positions(
    grid: list[list[str]]
) -> Generator[tuple[int, int], None, None]:
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
    def setup(self) -> None:
        self.input = [list(line) for line in self.raw_input.splitlines()]

    def part_1(self) -> int:
        checked_digits: set[tuple[int, int]] = set()
        numbers = []
        for i, j in generate_symbol_positions(self.input):
            for m, n in generate_neighbours(i, j):
                if self.input[m][n].isdigit():
                    if (m, n) in checked_digits:
                        continue
                    number, found_positions = get_full_number_from_position_in_line(
                        self.input[m], n
                    )
                    numbers.append(number)
                    checked_digits.update((m, p) for p in found_positions)
        return sum(numbers)

    def part_2(self) -> int:
        gear_ratios = []
        for i, j in generate_symbol_positions(self.input):
            if self.input[i][j] == "*":
                checked_digits: set[tuple[int, int]] = set()
                numbers = []
                for m, n in generate_neighbours(i, j):
                    if self.input[m][n].isdigit():
                        if (m, n) in checked_digits:
                            continue
                        number, found_positions = get_full_number_from_position_in_line(
                            self.input[m], n
                        )
                        numbers.append(number)
                        checked_digits.update((m, p) for p in found_positions)
                if len(numbers) == 2:  # Only 2 numbers in a gear ratio
                    gear_ratios.append(numbers[0] * numbers[1])
        return sum(gear_ratios)
