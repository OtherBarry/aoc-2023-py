from solutions.utilities.grid import (
    Direction,
    coordinate_in_bounds,
    generate_neighbours,
    input_to_char_grid,
    manhattan_distance,
)


def test_direction_from_nodes() -> None:
    assert Direction.from_nodes((0, 0), (0, 1)) == Direction.RIGHT
    assert Direction.from_nodes((0, 0), (1, 0)) == Direction.DOWN
    assert Direction.from_nodes((0, 0), (0, -1)) == Direction.LEFT
    assert Direction.from_nodes((0, 0), (-1, 0)) == Direction.UP


def test_direction_is_opposite() -> None:
    assert Direction.RIGHT.is_opposite(Direction.LEFT)
    assert not Direction.RIGHT.is_opposite(Direction.RIGHT)
    assert not Direction.RIGHT.is_opposite(Direction.UP)
    assert not Direction.RIGHT.is_opposite(Direction.DOWN)

    assert Direction.LEFT.is_opposite(Direction.RIGHT)
    assert not Direction.LEFT.is_opposite(Direction.LEFT)
    assert not Direction.LEFT.is_opposite(Direction.UP)
    assert not Direction.LEFT.is_opposite(Direction.DOWN)

    assert Direction.UP.is_opposite(Direction.DOWN)
    assert not Direction.UP.is_opposite(Direction.RIGHT)
    assert not Direction.UP.is_opposite(Direction.LEFT)
    assert not Direction.UP.is_opposite(Direction.UP)

    assert Direction.DOWN.is_opposite(Direction.UP)
    assert not Direction.DOWN.is_opposite(Direction.RIGHT)
    assert not Direction.DOWN.is_opposite(Direction.LEFT)
    assert not Direction.DOWN.is_opposite(Direction.DOWN)


def test_direction_apply() -> None:
    assert Direction.RIGHT.apply((0, 0)) == (0, 1)
    assert Direction.LEFT.apply((0, 0)) == (0, -1)
    assert Direction.UP.apply((0, 0)) == (-1, 0)
    assert Direction.DOWN.apply((0, 0)) == (1, 0)


def test_direction_apply_with_distance() -> None:
    assert Direction.RIGHT.apply((0, 0), 2) == (0, 2)
    assert Direction.LEFT.apply((0, 0), 2) == (0, -2)
    assert Direction.UP.apply((0, 0), 2) == (-2, 0)
    assert Direction.DOWN.apply((0, 0), 2) == (2, 0)


def test_input_to_char_grid() -> None:
    assert input_to_char_grid("a\nb\nc") == [["a"], ["b"], ["c"]]
    assert input_to_char_grid("abc\ndef") == [["a", "b", "c"], ["d", "e", "f"]]


def test_generate_neighbours() -> None:
    neighbours = list(generate_neighbours((0, 0)))
    assert len(neighbours) == 4
    assert (-1, 0) in neighbours
    assert (1, 0) in neighbours
    assert (0, -1) in neighbours
    assert (0, 1) in neighbours


def test_generate_neighbours_with_diagonal() -> None:
    neighbours = list(generate_neighbours((0, 0), diagonal=True))
    assert len(neighbours) == 8
    assert (-1, 0) in neighbours
    assert (1, 0) in neighbours
    assert (0, -1) in neighbours
    assert (0, 1) in neighbours
    assert (-1, -1) in neighbours
    assert (1, -1) in neighbours
    assert (-1, 1) in neighbours
    assert (1, 1) in neighbours


def test_coordinate_in_bounds() -> None:
    assert coordinate_in_bounds((0, 0), 1, 1)
    assert not coordinate_in_bounds((1, 1), 1, 1)
    assert not coordinate_in_bounds((-1, -1), 1, 1)


def test_coordinate_in_bounds_with_min() -> None:
    assert not coordinate_in_bounds((0, 0), 2, 2, 1, 1)
    assert coordinate_in_bounds((1, 1), 2, 2, 1, 1)
    assert not coordinate_in_bounds((2, 2), 2, 2, 1, 1)


def test_manhattan_distance() -> None:
    assert manhattan_distance((0, 0), (0, 0)) == 0
    assert manhattan_distance((0, 0), (1, 1)) == 2
    assert manhattan_distance((0, 0), (1, 0)) == 1
    assert manhattan_distance((0, 0), (0, 1)) == 1
    assert manhattan_distance((0, 0), (-1, 0)) == 1
    assert manhattan_distance((0, 0), (0, -1)) == 1
    assert manhattan_distance((0, 0), (-1, -1)) == 2
    assert manhattan_distance((0, 0), (1, -1)) == 2
    assert manhattan_distance((0, 0), (-1, 1)) == 2
