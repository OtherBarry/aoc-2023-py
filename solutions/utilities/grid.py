from collections.abc import Iterator
from enum import Enum

Coordinate = tuple[int, int]


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    UP = NORTH
    DOWN = SOUTH
    RIGHT = EAST
    LEFT = WEST

    @classmethod
    def from_nodes(cls, start: Coordinate, end: Coordinate) -> "Direction":
        return cls((end[0] - start[0], end[1] - start[1]))

    def is_opposite(self, other: "Direction") -> bool:
        return self.value[0] == -other.value[0] and self.value[1] == -other.value[1]  # type: ignore[comparison-overlap]

    def apply(self, pos: Coordinate, distance: int = 1) -> Coordinate:
        return pos[0] + (self.value[0] * distance), pos[1] + (self.value[1] * distance)


def input_to_char_grid(input_: str) -> list[list[str]]:
    """Convert the input to a 2D character list

    :param input_: The input
    :return: The 2D character list
    """
    return [list(line) for line in input_.splitlines()]


def generate_neighbours(
    coordinate: Coordinate, diagonal: bool = False
) -> Iterator[Coordinate]:
    """Generate the neighbours of a coordinate

    :param coordinate: The coordinate
    :param diagonal: Whether to include diagonal neighbours
    :return: The neighbours of the coordinate
    """
    i, j = coordinate
    yield i - 1, j
    yield i + 1, j
    yield i, j - 1
    yield i, j + 1
    if diagonal:
        yield i - 1, j - 1
        yield i + 1, j - 1
        yield i - 1, j + 1
        yield i + 1, j + 1


def coordinate_in_bounds(
    coordinate: Coordinate, y_max: int, x_max: int, y_min: int = 0, x_min: int = 0
) -> bool:
    """Check if a coordinate is in bounds of the given lines.

    :param coordinate: The coordinate to check.
    :param y_min: The minimum y value.
    :param y_max: The maximum y value.
    :param x_min: The minimum x value.
    :param x_max: The maximum x value.
    :returns: True if the coordinate is in bounds, False otherwise.
    """
    y, x = coordinate
    return y_min <= y < y_max and x_min <= x < x_max


def manhattan_distance(a: Coordinate, b: Coordinate) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
