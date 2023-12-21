import networkx as nx

from solutions.base import BaseSolution
from solutions.utilities.grid import Coordinate, Direction, coordinate_in_bounds


def generate_valid_connections(node: Coordinate, pipe_type: str) -> list[Coordinate]:  # noqa: PLR0911
    """Generate the valid connections for a node.

    :param node: The node to generate connections for.
    :param pipe_type: The type of pipe at the node.
    :returns: A list of valid connections.
    """
    if pipe_type == "|":
        return [Direction.NORTH.apply(node), Direction.SOUTH.apply(node)]
    if pipe_type == "-":
        return [Direction.EAST.apply(node), Direction.WEST.apply(node)]
    if pipe_type == "L":
        return [Direction.NORTH.apply(node), Direction.EAST.apply(node)]
    if pipe_type == "J":
        return [Direction.NORTH.apply(node), Direction.WEST.apply(node)]
    if pipe_type == "7":
        return [Direction.SOUTH.apply(node), Direction.WEST.apply(node)]
    if pipe_type == "F":
        return [Direction.SOUTH.apply(node), Direction.EAST.apply(node)]
    if pipe_type == "S":
        return [
            Direction.NORTH.apply(node),
            Direction.SOUTH.apply(node),
            Direction.EAST.apply(node),
            Direction.WEST.apply(node),
        ]
    return []


def node_is_even(node: Coordinate) -> bool:
    """Check if all coords of a node are even.

    :param node: The node to check.
    :returns: True if the node is even, False otherwise.
    """
    y, x = node
    return y % 2 == 0 and x % 2 == 0


class Solution(BaseSolution):
    def setup(self) -> None:  # noqa: C901
        lines = self.raw_input.splitlines()
        self.height = len(lines)
        self.width = len(lines[0])
        self.start_node = None

        all_pipes = nx.Graph()
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                value = lines[i][j]
                node = (i, j)
                if value == ".":
                    continue
                if value == "S":
                    self.start_node = node
                    continue
                for con in generate_valid_connections(node, value):
                    if coordinate_in_bounds(con, self.height, self.width):
                        connections_connections = generate_valid_connections(
                            con, lines[con[0]][con[1]]
                        )
                        if node in connections_connections:
                            all_pipes.add_edge(node, con)
        self.main_loop_graph = nx.bfs_tree(all_pipes, self.start_node)

        self.ground_graph = nx.grid_2d_graph(self.height * 2, self.width * 2)
        for node in self.main_loop_graph.nodes:
            external_node = (node[0] * 2, node[1] * 2)
            self.ground_graph.remove_node(external_node)
            for con in generate_valid_connections(
                external_node, lines[node[0]][node[1]]
            ):
                if con in self.ground_graph:
                    self.ground_graph.remove_node(con)

    def part_1(self) -> int:
        paths: dict[Coordinate, int] = nx.shortest_path_length(
            self.main_loop_graph, self.start_node
        )
        return max(paths.values())

    def part_2(self) -> int:
        total_contained = 0
        for component in nx.connected_components(self.ground_graph):
            if all(
                coordinate_in_bounds(
                    n, (self.height * 2) - 1, (self.width * 2) - 1, y_min=1, x_min=1
                )
                for n in component
            ):
                total_contained += sum(1 for n in component if node_is_even(n))
        return total_contained
