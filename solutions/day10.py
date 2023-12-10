import networkx as nx

from solutions.base import BaseSolution

Coord = tuple[int, int]


def generate_valid_connections(node: Coord, pipe_type: str) -> list[Coord]:
    """Generate the valid connections for a node.

    :param node: The node to generate connections for.
    :param pipe_type: The type of pipe at the node.
    :returns: A list of valid connections.
    """
    y, x = node
    north, east, south, west = (y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)
    if pipe_type == "|":
        return [north, south]
    if pipe_type == "-":
        return [east, west]
    if pipe_type == "L":
        return [north, east]
    if pipe_type == "J":
        return [north, west]
    if pipe_type == "7":
        return [south, west]
    if pipe_type == "F":
        return [south, east]
    if pipe_type == "S":
        return [north, south, east, west]
    return []


def node_in_bounds(node: Coord, y_min: int, y_max: int, x_min: int, x_max: int) -> bool:
    """Check if a node is in bounds of the given lines.

    :param node: The node to check.
    :param y_min: The minimum y value.
    :param y_max: The maximum y value.
    :param x_min: The minimum x value.
    :param x_max: The maximum x value.
    :returns: True if the node is in bounds, False otherwise.
    """
    y, x = node
    return y_min <= y < y_max and x_min <= x < x_max


def node_is_even(node: Coord) -> bool:
    """Check if all coords of a node are even.

    :param node: The node to check.
    :returns: True if the node is even, False otherwise.
    """
    y, x = node
    return y % 2 == 0 and x % 2 == 0


class Solution(BaseSolution):
    def setup(self) -> None:
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
                    if node_in_bounds(con, 0, self.height, 0, self.width):
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
        paths: dict[Coord, int] = nx.shortest_path_length(
            self.main_loop_graph, self.start_node
        )
        return max(paths.values())

    def part_2(self) -> int:
        total_contained = 0
        for component in nx.connected_components(self.ground_graph):
            if all(
                node_in_bounds(n, 1, (self.height * 2) - 1, 1, (self.width * 2) - 1)
                for n in component
            ):
                total_contained += sum(1 for n in component if node_is_even(n))
        return total_contained
