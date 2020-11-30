import re
from typing import Iterator

from aoc.common import input
from aoc.common import solution


def has_abba(s: str) -> bool:
    if len(s) < 4:
        return False
    for i in range(len(s) - 3):
        if s[i] == s[i + 3] and s[i + 1] == s[i + 2] and s[i] != s[i + 1]:
            return True
    return False


def all_aba(s: str) -> Iterator[str]:
    if len(s) < 3:
        return
    for i in range(len(s) - 2):
        if s[i] == s[i + 2] and s[i] != s[i + 1]:
            yield s[i + 1] + s[i] + s[i + 1]


def check_ip_aba(ip: str) -> bool:
    parts = re.split(r"\[|]", ip)
    out_block = [parts[i] for i in range(0, len(parts), 2)]
    in_block = [parts[i] for i in range(1, len(parts), 2)]

    return any(
        bab in in_part
        for out_part in out_block
        for bab in all_aba(out_part)
        for in_part in in_block
    )


@solution.part_one(year=2016, problem=7)
def part_one(data: input.Tokenized["\n"]) -> int:
    return sum(
        has_abba(ip)
        and not any(has_abba(hn.group(1)) for hn in re.finditer(r"\[(\w+?)]", ip))
        for ip in data
    )


@solution.part_two(year=2016, problem=7)
def part_two(data: input.Tokenized["\n"]) -> int:
    return sum(map(check_ip_aba, data))
