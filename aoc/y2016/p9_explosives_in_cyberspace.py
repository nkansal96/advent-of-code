from typing import Tuple

from aoc.common import solution


def parse_expansion(s: str) -> Tuple[int, int, int]:
    s = s[1 : s.find(")")]
    n, m = map(int, s.split("x"))
    return n, m, len(s) + 2


def decompressed_length(s: str) -> int:
    i = 0
    total = 0
    while i < len(s):
        if s[i] == "(":
            n, m, k = parse_expansion(s[i:])
            total += m * n
            i += k + n
        else:
            total += 1
            i += 1
    return total


def decompressed_length_v2(s: str) -> int:
    i = 0
    total = 0
    while i < len(s):
        if s[i] == "(":
            n, m, k = parse_expansion(s[i:])
            total += m * decompressed_length_v2(s[i + k : i + k + n])
            i += k + n
        else:
            total += 1
            i += 1
    return total


@solution.part_one(year=2016, problem=9)
def part_one(data: str) -> int:
    return decompressed_length(data)


@solution.part_two(year=2016, problem=9)
def part_two(data: str) -> int:
    return decompressed_length_v2(data)
