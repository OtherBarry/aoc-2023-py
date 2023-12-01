import argparse
from importlib import import_module
from pathlib import Path

from solutions.base import BaseSolution
from timer import Timer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problems", nargs="*", type=int, help="The problems to run")
    args = parser.parse_args()
    print("Running problems")

    with Timer() as timer:
        for problem in args.problems:
            print(f"\nProblem {problem}:")
            input_path = Path(f"inputs/{problem:02d}.txt")
            solution_class: type[BaseSolution] = import_module(
                f"solutions.day{problem:02d}"
            ).Solution
            solution = solution_class(input_path)
            solution.run()
    print(f"\nTotal time: {timer}")
