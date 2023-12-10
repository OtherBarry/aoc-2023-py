# Advent of Code 2023

This repository contains solutions for Advent of Code 2023 in Python.

## Prerequisites

- Python 3.11 or higher

## Running the Solutions

The solutions can be run from the command line using the `main.py` script. You can specify which problems to run by passing their numbers as arguments.

For example, to run the solutions for problems 1, 2, and 3, you would use the following command:

```bash
python main.py 1 2 3
```

This will run the solutions for problems 1, 2, and 3, in that order.

## Solution Output

The output of each solution is printed to the console, along with the time taken to run each step. The total time taken to run all specified solutions is also printed at the end.

## Adding New Solutions

New solutions should be added to the `solutions` directory. Each solution should be in its own Python file named `dayXX.py`, where `XX` is the problem number.

Each solution file should define a `Solution` class that inherits from `BaseSolution`. This class should implement the `setup`, `part_1`, and `part_2` methods. See the existing solution files for examples.

The input for each problem should be placed in the `inputs` directory in a file named `XX.txt`, where `XX` is the problem number.

## Testing Solutions

Tests for the solutions can be added to the `tests` directory. Each test file should be named `test_dayXX.py`, where `XX` is the problem number. See the existing test files for examples of how to write tests for the solutions.
