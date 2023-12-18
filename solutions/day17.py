from collections.abc import Iterator
from enum import Enum
from heapq import heappop, heappush
from itertools import count
from typing import Optional

import networkx as nx

from solutions.base import BaseSolution

Coord = tuple[int, int]
Node = tuple[int, int, Optional["Direction"], int]


class Direction(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)

    @classmethod
    def from_node(cls, node: Coord, next_node: Coord) -> "Direction":
        return cls((next_node[0] - node[0], next_node[1] - node[1]))

    def is_opposite(self, other: "Direction") -> bool:
        return self.value[0] == -other.value[0] and self.value[1] == -other.value[1]  # type: ignore[comparison-overlap]


def manhattan_distance(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def generate_neighbours(node: Coord) -> Iterator[Coord]:
    for direction in Direction:
        yield node[0] + direction.value[0], node[1] + direction.value[1]


def sum_path(graph: nx.Graph, path: list[Node]) -> int:
    return sum(graph.nodes[node]["weight"] for node in path[1:])


def create_graph(data: list[str], min_steps: int, max_steps: int) -> nx.Graph:  # noqa: C901
    height = len(data)
    width = len(data[0])

    def is_valid(node: Coord) -> bool:
        return 0 <= node[0] < height and 0 <= node[1] < width

    graph = nx.DiGraph()
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            weight = int(char)
            neighbours = [n for n in generate_neighbours((i, j)) if is_valid(n)]
            if i == 0 and j == 0:
                graph.add_node((i, j, None, 0), weight=0)
                for neighbour in neighbours:
                    start_direction = Direction.from_node((i, j), neighbour)
                    graph.add_edge(
                        (i, j, None, 0),
                        (neighbour[0], neighbour[1], start_direction, 1),
                    )
            for direction in Direction:
                for steps in range(1, max_steps + 1):
                    graph.add_node((i, j, direction, steps), weight=weight)
                    for neighbour in neighbours:
                        neighbour_direction = Direction.from_node((i, j), neighbour)
                        if neighbour_direction.is_opposite(direction):
                            continue
                        if neighbour_direction != direction:
                            if steps >= min_steps:
                                graph.add_edge(
                                    (i, j, direction, steps),
                                    (
                                        neighbour[0],
                                        neighbour[1],
                                        neighbour_direction,
                                        1,
                                    ),
                                )
                        elif steps < max_steps:
                            graph.add_edge(
                                (i, j, direction, steps),
                                (neighbour[0], neighbour[1], direction, steps + 1),
                            )
    return graph


def astar_path(graph: nx.Graph, source_coord: Coord, target_coord: Coord) -> list[Node]:
    """Copied from networkx's A* implementation.

    Modified to:
    - use coordinates as start/end nodes
    - use edge weight property as cost
    - use manhattan distance as heuristic
    """
    source = (source_coord[0], source_coord[1], None, 0)
    adjacency_matrix = graph._adj  # noqa: SLF001
    c = count()
    queue = [(0, next(c), source, 0, None)]
    enqueued: dict[Node, tuple[int, int]] = {}
    explored: dict[Node, Node | None] = {}

    while queue:
        _, __, curnode, dist, parent = heappop(queue)

        i, j, *_ = curnode
        if (i, j) == target_coord:
            path: list[Node] = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path

        if curnode in explored:
            if explored[curnode] is None:
                continue
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue

        explored[curnode] = parent

        for neighbor in adjacency_matrix[curnode]:
            cost = graph.nodes[neighbor]["weight"]
            ncost = dist + cost
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = manhattan_distance(neighbor, target_coord)
            enqueued[neighbor] = ncost, h
            heappush(queue, (ncost + h, next(c), neighbor, ncost, curnode))  # type: ignore[misc]

    msg = f"Node {target_coord} not reachable from {source_coord}"
    raise nx.NetworkXNoPath(msg)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.data = self.raw_input.splitlines()
        self.height = len(self.data)
        self.width = len(self.data[0])

    def part_1(self) -> int:
        graph = create_graph(self.data, 0, 3)
        path = astar_path(graph, (0, 0), (self.height - 1, self.width - 1))
        return sum_path(graph, path)

    def part_2(self) -> int:
        graph = create_graph(self.data, 4, 10)
        path = astar_path(graph, (0, 0), (self.height - 1, self.width - 1))
        return sum_path(graph, path)
