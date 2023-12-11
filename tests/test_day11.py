from solutions.day11 import expand_empty_space


def test_expand_empty_space() -> None:
    start = "...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#....."
    as_map = [list(row) for row in start.splitlines()]
    expanded_map = expand_empty_space(as_map)
    expanded_str = "\n".join("".join(row) for row in expanded_map)
    assert (
        expanded_str
        == "....#........\n.........#...\n#............\n.............\n.............\n........#....\n.#...........\n............#\n.............\n.............\n.........#...\n#....#......."
    )
