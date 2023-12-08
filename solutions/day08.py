from collections.abc import Callable
from math import lcm

from solutions.base import BaseSolution


class Node:
    def __init__(self, value: str) -> None:
        self.value = value
        self._left: Node | None = None
        self._right: Node | None = None

    @property
    def left(self) -> "Node":
        if self._left is None:
            msg = "Node has no left node"
            raise ValueError(msg)
        return self._left

    @left.setter
    def left(self, node: "Node") -> None:
        self._left = node

    @property
    def right(self) -> "Node":
        if self._right is None:
            msg = "Node has no right node"
            raise ValueError(msg)
        return self._right

    @right.setter
    def right(self, node: "Node") -> None:
        self._right = node


class Tree:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}

    def add_node(self, node_id: str, left_id: str, right_id: str) -> None:
        node = self.nodes.setdefault(node_id, Node(node_id))
        node.left = self.nodes.setdefault(left_id, Node(left_id))
        node.right = self.nodes.setdefault(right_id, Node(right_id))


def calculate_number_of_moves(
    start: Node, moves: str, is_end_node: Callable[[str], bool]
) -> int:
    current = start
    move_count = 0
    while not is_end_node(current.value):
        next_move = moves[move_count % len(moves)]
        current = current.left if next_move == "L" else current.right
        move_count += 1
    return move_count


class Solution(BaseSolution):
    def setup(self) -> None:
        lines = self.raw_input.splitlines()
        self.nodes: dict[str, Node] = {}
        for line in lines[2:]:
            node = self.nodes.setdefault(line[:3], Node(line[:3]))
            node.left = self.nodes.setdefault(line[7:10], Node(line[7:10]))
            node.right = self.nodes.setdefault(line[12:15], Node(line[12:15]))
        self.moves = lines[0]

    def part_1(self) -> int:
        return calculate_number_of_moves(
            self.nodes["AAA"], self.moves, lambda x: x == "ZZZ"
        )

    def part_2(self) -> int:
        current_nodes = [node for node in self.nodes.values() if node.value[-1] == "A"]
        move_numbers = [
            calculate_number_of_moves(node, self.moves, lambda x: x[-1] == "Z")
            for node in current_nodes
        ]
        return lcm(*move_numbers)
