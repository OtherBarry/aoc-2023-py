from collections.abc import Iterable
from enum import Enum

import numpy as np
import numpy.typing as npt

from solutions.base import BaseSolution


class Direction(Enum):
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)

    def apply(self, pos: tuple[int, int]) -> tuple[int, int]:
        return pos[0] + self.value[0], pos[1] + self.value[1]


DIR_LETTER_MAP = {
    "R": Direction.RIGHT,
    "L": Direction.LEFT,
    "U": Direction.UP,
    "D": Direction.DOWN,
}

DIR_DIGIT_MAP = {
    "0": Direction.RIGHT,
    "1": Direction.DOWN,
    "2": Direction.LEFT,
    "3": Direction.UP,
}


def calculate_area(data: Iterable[tuple[Direction, int]]) -> int:
    current = (0, 0)
    x_values = [0]
    y_values = [0]
    visited = {current}
    for direction, distance in data:
        for _ in range(distance):
            current = direction.apply(current)
            visited.add(current)
        x_values.append(current[0])
        y_values.append(current[1])

    # Pick's theorem
    area = shoelace_theorem_area(np.array(x_values), np.array(y_values))
    boundary_points = len(visited)
    interior_points = area + 1 - boundary_points // 2
    return int(interior_points + boundary_points)


def shoelace_theorem_area(x: npt.NDArray[int], y: npt.NDArray[int]) -> float:  # type: ignore[type-var]
    x_ = x - x.mean()
    y_ = y - y.mean()
    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:])
    return 0.5 * np.abs(main_area + correction)  # type: ignore[no-any-return]


def parse_hex(hex_code: str) -> tuple[Direction, int]:
    direction = DIR_DIGIT_MAP[hex_code[-1]]
    distance = int(hex_code[:-1], 16)
    return direction, distance


class Solution(BaseSolution):
    def setup(self) -> None:
        pass

    def part_1(self) -> int:
        data = []
        for line in self.raw_input.splitlines():
            dir_char, raw_distance, _ = line.split()
            data.append((DIR_LETTER_MAP[dir_char], int(raw_distance)))
        return calculate_area(data)

    def part_2(self) -> int:
        return calculate_area(
            parse_hex(line[-7:-1]) for line in self.raw_input.splitlines()
        )
