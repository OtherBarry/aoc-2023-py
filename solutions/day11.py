from itertools import combinations

from solutions.base import BaseSolution


def get_empty_rows_and_columns(map_: list[list[str]]) -> tuple[set[int], set[int]]:
    empty_rows = {i for i, row in enumerate(map_) if all(value == "." for value in row)}
    empty_columns = {
        j for j in range(len(map_[0])) if all(row[j] == "." for row in map_)
    }
    return empty_rows, empty_columns


class Solution(BaseSolution):
    def count_steps(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> tuple[int, int]:
        steps = 0
        empty_steps = 0
        for y in range(min(start[0], end[0]), max(start[0], end[0])):
            if y in self.empty_rows:
                empty_steps += 1
            else:
                steps += 1
        for x in range(min(start[1], end[1]), max(start[1], end[1])):
            if x in self.empty_columns:
                empty_steps += 1
            else:
                steps += 1
        return steps, empty_steps

    def setup(self) -> None:
        base_map = [list(row) for row in self.raw_input.splitlines()]
        self.empty_rows, self.empty_columns = get_empty_rows_and_columns(base_map)

        self.galaxies = []
        for i, row in enumerate(base_map):
            for j, value in enumerate(row):
                if value == "#":
                    self.galaxies.append((i, j))

        self.num_steps = 0
        self.num_empty_steps = 0
        for start, end in combinations(self.galaxies, 2):
            steps, empty_steps = self.count_steps(start, end)
            self.num_steps += steps
            self.num_empty_steps += empty_steps

    def part_1(self) -> int:
        return self.num_steps + (self.num_empty_steps * 2)

    def part_2(self) -> int:
        return self.num_steps + (self.num_empty_steps * 1_000_000)
