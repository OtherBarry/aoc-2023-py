from solutions.base import BaseSolution


class Solution(BaseSolution):
    STRING_DIGIT_MAP = {
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

    @classmethod
    def extract_digit(
        cls, line: str, include_words: bool = False, reverse: bool = False
    ) -> str:
        """Extract the first digit from a string, or the last if reverse is True

        :param line: The string to extract the digit from
        :param include_words: Whether to allow digits as words (e.g. "one" -> "1")
        :param reverse: Whether to extract the last digit instead of the first
        :return: The first (or last) digit in the string
        """
        range_ = range(len(line) - 1, -1, -1) if reverse else range(len(line))
        for i in range_:
            if line[i].isdigit():
                return line[i]
            if include_words:
                for word, digit in cls.STRING_DIGIT_MAP.items():
                    if line[i:].startswith(word):
                        return digit
        msg = "No digit found"
        raise ValueError(msg)

    @classmethod
    def calculate_calibration_value(cls, line: str, include_words: bool) -> int:
        """Calculate the calibration value of a string

        :param line: The string to calculate the calibration value of
        :param include_words: Whether to allow digits as words (e.g. "one" -> "1")
        :return: The calibration value of the string
        """
        first = cls.extract_digit(line, include_words=include_words)
        last = cls.extract_digit(line, include_words=include_words, reverse=True)
        return int(first + last)

    def setup(self) -> None:
        self.lines = self.raw_input.splitlines()

    def part_1(self) -> int:
        calibration_values = [
            self.calculate_calibration_value(line, include_words=False)
            for line in self.lines
        ]
        return sum(calibration_values)

    def part_2(self) -> int:
        calibration_values = [
            self.calculate_calibration_value(line, include_words=True)
            for line in self.lines
        ]
        return sum(calibration_values)
