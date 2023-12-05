from collections import defaultdict

from solutions.base import BaseSolution


def calculate_winning_values(line: str) -> tuple[int, int]:
    """Find the number of winning values in a scratch card.

    :param line: The line to convert
    :return: The card number and the number of winning values
    """
    card_id = int(line[4:8])
    winners = {int(line[i : i + 2]) for i in range(10, 40, 3)}
    values = {int(line[i : i + 2]) for i in range(42, 116, 3)}
    num_winning_values = len(winners & values)
    return card_id, num_winning_values


class Solution(BaseSolution):
    def setup(self) -> None:
        self.cards: dict[int, int] = {}
        for line in self.raw_input.splitlines():
            card_id, n_winners = calculate_winning_values(line)
            self.cards[card_id] = n_winners

    def part_1(self) -> int:
        winner_points = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
        total = 0
        for n_winners in self.cards.values():
            total += winner_points[n_winners]
        return total

    def part_2(self) -> int:
        count: dict[int, int] = defaultdict(lambda: 0)
        for i in range(1, len(self.cards) + 1):
            count[i] += 1
            for j in range(i + 1, i + 1 + self.cards[i]):
                count[j] += count[i]
        return sum(count.values())
