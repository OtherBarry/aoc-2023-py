from itertools import combinations

import numpy as np

from solutions.base import BaseSolution

Coord = tuple[int, int]


def manhattan_distance(a: Coord, b: Coord) -> int:
    return sum(abs(a[i] - b[i]) for i in range(len(a)))


def expand_empty_space(raw_map: list[list[str]]) -> list[list[str]]:
    np_map = np.array(raw_map)

    # expand rows
    rows_to_insert = [i for i, row in enumerate(np_map) if "#" not in row]
    inserts = 0
    for i in rows_to_insert:
        np_map = np.insert(np_map, i + inserts + 1, np_map[i + inserts], axis=0)
        inserts += 1

    # expand columns
    cols_to_insert = [i for i, col in enumerate(np_map.T) if "#" not in col]
    inserts = 0
    for i in cols_to_insert:
        np_map = np.insert(np_map, i + inserts + 1, np_map[:, i + inserts], axis=1)
        inserts += 1

    # convert back to list of lists
    return np_map.tolist()  # type: ignore[no-any-return]


class Solution(BaseSolution):
    def setup(self) -> None:
        base_map = [list(row) for row in self.raw_input.splitlines()]
        self.map = expand_empty_space(base_map)

    def part_1(self) -> int:
        galaxies = []
        for i, row in enumerate(self.map):
            for j, value in enumerate(row):
                if value == "#":
                    galaxies.append((i, j))

        pairs = combinations(galaxies, 2)
        return sum(manhattan_distance(*pair) for pair in pairs)

    def part_2(self) -> int:
        return -1
