import networkx as nx

from solutions.base import BaseSolution
from solutions.utilities.grid import (
    Direction,
    generate_neighbours,
    input_to_char_grid,
    manhattan_distance,
)

SLOPE_DIRECTION_MAP = {
    "<": Direction.LEFT,
    ">": Direction.RIGHT,
    "^": Direction.UP,
    "v": Direction.DOWN,
}


def generate_directed_graph(grid: list[list[str]]) -> nx.DiGraph:
    len(grid)
    len(grid[0])
    graph = nx.DiGraph()
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            match char:
                case "#":
                    continue
                case ".":
                    for neighbour in generate_neighbours((i, j)):
                        try:
                            if grid[neighbour[0]][neighbour[1]] != "#":
                                graph.add_edge((i, j), neighbour)
                        except IndexError:
                            continue
                case _:
                    graph.add_edge((i, j), SLOPE_DIRECTION_MAP[char].apply((i, j)))

    return graph


def generated_undirected_graph(grid: list[list[str]]) -> nx.Graph:
    height = len(grid)
    width = len(grid[0])
    graph = nx.grid_2d_graph(height, width)
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            match char:
                case "#":
                    graph.remove_node((i, j))
                case _:
                    pass
    return graph


def prune_graph(graph: nx.Graph) -> nx.Graph:
    """Prune a graph by removing nodes with only two neighbours, and connecting the neighbours."""

    nx.set_edge_attributes(graph, 1, "weight")

    def is_node_to_prune(node: tuple[int, int]) -> bool:
        return len(graph[node]) == 2

    def prune_node(node: tuple[int, int]) -> None:
        neighbours = list(graph[node])
        new_weight = (
            graph.edges[neighbours[0], node]["weight"]
            + graph.edges[neighbours[1], node]["weight"]
        )
        graph.remove_node(node)
        graph.add_edge(*neighbours, weight=new_weight)

    nodes_to_prune = [node for node in graph if is_node_to_prune(node)]
    while nodes_to_prune:
        for node in nodes_to_prune:
            prune_node(node)
        nodes_to_prune = [node for node in graph if is_node_to_prune(node)]
    return graph


def path_length(path: list[tuple[int, int]]) -> int:
    return sum(manhattan_distance(path[i - 1], path[i]) for i in range(1, len(path)))


class Solution(BaseSolution):
    def setup(self) -> None:
        self.grid = input_to_char_grid(self.raw_input)
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.start = (0, 1)
        self.end = (self.height - 1, self.width - 2)

    def part_1(self) -> int:
        graph = generate_directed_graph(self.grid)
        paths = nx.all_simple_paths(graph, self.start, self.end)
        return max(len(path) for path in paths) - 1

    def part_2(self) -> int:
        graph = generated_undirected_graph(self.grid)
        graph = prune_graph(graph)
        paths = nx.all_simple_paths(graph, self.start, self.end)
        return max(nx.path_weight(graph, path, "weight") for path in paths)  # type: ignore[no-any-return]
