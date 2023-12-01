from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from timer import Timer


class BaseSolution(ABC):
    def __init__(self, input_path: Path) -> None:
        with input_path.open() as f:
            self.raw_input = f.read()

    def setup(self) -> None:  # noqa: B027
        pass

    @abstractmethod
    def part_1(self) -> Any:
        pass

    @abstractmethod
    def part_2(self) -> Any:
        pass

    def run(self) -> None:
        with Timer() as timer:
            self.setup()
        print(f"\tSetup run in {timer}")
        with Timer() as timer:
            p1_result = self.part_1()
        print(f"\tPart 1 ({timer}): {p1_result}")
        with Timer() as timer:
            p2_result = self.part_2()
        print(f"\tPart 2 ({timer}): {p2_result}")
