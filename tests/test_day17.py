from solutions.day17 import Direction, Node, astar_path, create_graph, sum_path


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


example_path = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (0, 5),
    (0, 6),
    (0, 7),
    (0, 8),
    (1, 8),
    (2, 8),
    (2, 9),
    (2, 10),
    (3, 10),
    (4, 10),
    (4, 11),
    (5, 11),
    (6, 11),
    (7, 11),
    (7, 12),
    (8, 12),
    (9, 12),
    (10, 12),
    (10, 11),
    (11, 11),
    (12, 11),
    (12, 12),
]

example = "2413432311323\n3215453535623\n3255245654254\n3446585845452\n4546657867536\n1438598798454\n4457876987766\n3637877979653\n4654967986887\n4564679986453\n1224686865563\n2546548887735\n4322674655533"


def test_example_part_1() -> None:
    data = example.splitlines()
    graph = create_graph(data, 0, 3)
    path = astar_path(graph, (0, 0), (len(data) - 1, len(data[0]) - 1))
    print(path)
    print_path(path)
    assert sum_path(graph, path) == 102


def print_path(path: list[Node]) -> None:
    path_coords = {(i, j) for i, j, *_ in path}
    print()
    for i in range(13):
        for j in range(13):
            node = (i, j)
            if node in path_coords:
                print("🟩", end="")
            else:
                print("🟦", end="")
        print()
