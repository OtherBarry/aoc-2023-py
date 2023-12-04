from collections.abc import Generator

import networkx as nx

from solutions.base import BaseSolution


def generate_neighbours(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    """Generate the neighbours of a coordinate

    :param x: The x coordinate
    :param y: The y coordinate
    :return: The neighbours of the coordinate
    """
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x - 1, y + 1
    yield x, y + 1
    yield x + 1, y + 1


def get_full_number_from_position_in_line(
    line: list[str], position: int
) -> tuple[int, list[int]]:
    """Get the full number at a position in a line

    :param line: The line
    :param position: The position in the line
    :return: The number at the position
    """
    start = position
    for i in range(position - 1, -1, -1):
        if not line[i].isdigit():
            break
        start = i

    end = position
    for i in range(position + 1, len(line)):
        if not line[i].isdigit():
            break
        end = i

    return int("".join(line[start : end + 1])), list(range(start, end + 1))


def generate_symbol_positions(
    grid: list[list[str]]
) -> Generator[tuple[int, int], None, None]:
    """Generate the positions of symbols in a grid

    :param grid: The grid
    :return: The positions of symbols in the grid
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "." or grid[i][j].isdigit():
                continue
            yield i, j


class Solution(BaseSolution):
    def setup(self) -> None:
        grid_input = [list(line) for line in self.raw_input.splitlines()]
        graph = nx.Graph()
        for i in range(len(grid_input)):
            for j in range(len(grid_input[i])):
                value = grid_input[i][j]
                if value == ".":
                    continue
                graph.add_node((i, j), value=value)

        for i, j in graph.nodes:
            for m, n in generate_neighbours(i, j):
                if (m, n) not in graph.nodes:
                    continue
                graph.add_edge((i, j), (m, n))

        combined_nodes = set()
        for i, j in list(graph.nodes):
            if grid_input[i][j].isdigit() and (i, j) not in combined_nodes:
                new_value, node_set = get_full_number_from_position_in_line(
                    grid_input[i], j
                )
                node_list = [(i, n) for n in node_set]
                for joinee in node_list[1:]:
                    nx.contracted_nodes(
                        graph, node_list[0], joinee, self_loops=False, copy=False
                    )
                graph.nodes[node_list[0]]["value"] = str(new_value)
                combined_nodes.update(node_list)
        self.graph = graph

    def part_1(self) -> int:
        part_number_sum = 0
        for coords, data in self.graph.nodes.items():
            node_value = data["value"]
            if node_value.isdigit():
                for n in self.graph.neighbors(coords):
                    if not self.graph.nodes[n]["value"].isdigit():
                        part_number_sum += int(node_value)
                        break
        return part_number_sum

    def part_2(self) -> int:
        gear_ratio_sum = 0
        for coords, data in self.graph.nodes.items():
            if data["value"] == "*":
                neighbours = []
                for n in self.graph.neighbors(coords):
                    n_value = self.graph.nodes[n]["value"]
                    if n_value.isdigit():
                        neighbours.append(n_value)
                    if len(neighbours) > 2:
                        break
                else:
                    if len(neighbours) == 2:
                        gear_ratio_sum += int(neighbours[0]) * int(neighbours[1])
        return gear_ratio_sum
