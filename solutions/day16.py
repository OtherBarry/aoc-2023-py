import sys
from enum import Enum

import networkx as nx

from solutions.base import BaseSolution


class Direction(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)


def char_to_dir(char: str, direction: Direction) -> list[Direction]:  # noqa: PLR0911
    match (char, direction):
        # continue in same direction
        case (
            (".", _)
            | ("-", Direction.RIGHT)
            | ("-", Direction.LEFT)
            | ("|", Direction.UP)
            | ("|", Direction.DOWN)
        ):
            return [direction]

        # bounce off mirror
        case ("\\", Direction.RIGHT) | ("/", Direction.LEFT):
            return [Direction.DOWN]
        case ("\\", Direction.LEFT) | ("/", Direction.RIGHT):
            return [Direction.UP]
        case ("\\", Direction.UP) | ("/", Direction.DOWN):
            return [Direction.LEFT]
        case ("\\", Direction.DOWN) | ("/", Direction.UP):
            return [Direction.RIGHT]

        # split
        case ("-", Direction.UP) | ("-", Direction.DOWN):
            return [Direction.LEFT, Direction.RIGHT]
        case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
            return [Direction.UP, Direction.DOWN]
        case _:
            msg = f"Invalid char/direction: {char}/{direction}"
            raise ValueError(msg)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.map = [list(row) for row in self.raw_input.splitlines()]
        self.height = len(self.map)
        self.width = len(self.map[0])

        # this is almost certainly a sign of doing the wrong thing
        sys.setrecursionlimit((self.height * self.width) * 4)

    def count_energised_tiles(
        self, start_pos: tuple[int, int], start_dir: Direction
    ) -> int:
        graph = nx.DiGraph()

        def update_graph(pos: tuple[int, int], direction: Direction) -> None:
            next_pos = (pos[0] + direction.value[0], pos[1] + direction.value[1])

            if graph.has_edge(pos, next_pos) or not (
                0 <= next_pos[0] < self.height and 0 <= next_pos[1] < self.width
            ):
                # next pos is out of bounds, or we've already visited it from this pos
                return
            graph.add_edge(pos, next_pos)
            char = self.map[next_pos[0]][next_pos[1]]
            for new_dir in char_to_dir(char, direction):
                update_graph(next_pos, new_dir)

        update_graph(start_pos, start_dir)
        return graph.number_of_nodes()  # type: ignore[no-any-return]

    def part_1(self) -> int:
        return self.count_energised_tiles((0, 0), Direction.RIGHT)

    def part_2(self) -> int:
        height = len(self.map)
        width = len(self.map[0])
        most_illumination = 0
        for i in range(self.height):
            most_illumination = max(
                most_illumination,
                self.count_energised_tiles((i, 0), Direction.RIGHT),
                self.count_energised_tiles((i, width - 1), Direction.LEFT),
            )
        for j in range(self.width):
            most_illumination = max(
                most_illumination,
                self.count_energised_tiles((0, j), Direction.DOWN),
                self.count_energised_tiles((height - 1, j), Direction.UP),
            )
        return most_illumination
