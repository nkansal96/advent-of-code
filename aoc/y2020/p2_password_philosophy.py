from collections import Counter
from typing import Tuple

import itertools
import re

from aoc.common import input
from aoc.common import solution


def parse_password(line: str) -> Tuple[int, int, str, str]:
    m = re.match(r"(\d+)-(\d+) (\w+): (\w+)", line)
    return int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)


@solution.part_one(year=2020, problem=2)
def _(data: input.Tokenized[input.NL]) -> int:
    def is_password_valid(lower: int, upper: int, ch: str, pw: str):
        return lower <= Counter(pw).get(ch, 0) <= upper

    passwords = data.each_token_as(parse_password)
    return sum(itertools.starmap(is_password_valid, passwords))


@solution.part_two(year=2020, problem=2)
def _(data: input.Tokenized[input.NL]) -> int:
    def is_password_valid(lower: int, upper: int, ch: str, pw: str):
        return (pw[lower - 1] == ch) ^ (pw[upper - 1] == ch)

    passwords = data.each_token_as(parse_password)
    return sum(itertools.starmap(is_password_valid, passwords))
