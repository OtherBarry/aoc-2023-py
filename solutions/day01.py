from solutions.base import BaseSolution

string_digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def extract_digits(line: str) -> int:
    digits = "".join([c for c in line if c.isdigit()])
    return int(digits[0] + digits[-1])


def extract_first_digit_or_digit_word(line: str, reverse: bool = False) -> str:
    range_ = range(len(line) - 1, -1, -1) if reverse else range(len(line))
    for i in range_:
        if line[i].isdigit():
            return line[i]
        for word, digit in string_digit_map.items():
            if line[i:].startswith(word):
                return digit
    msg = "No digit found"
    raise ValueError(msg)


def extract_digits_and_digits_as_words(line: str) -> int:
    first = extract_first_digit_or_digit_word(line)
    last = extract_first_digit_or_digit_word(line, reverse=True)
    return int(first + last)


class Solution(BaseSolution):
    def setup(self) -> None:
        self.lines = self.raw_input.splitlines()

    def part_1(self) -> int:
        calibration_values = [extract_digits(line) for line in self.lines]
        return sum(calibration_values)

    def part_2(self) -> int:
        calibration_values = [
            extract_digits_and_digits_as_words(line) for line in self.lines
        ]
        return sum(calibration_values)
