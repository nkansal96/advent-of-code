from collections import defaultdict
from typing import Callable

from aoc.common import solution


def solve(data: str, is_nice: Callable[[str], bool]) -> int:
    return sum(1 for s in data.split("\n") if is_nice(s))


@solution.part_one(year=2015, problem=5)
def part_one(data: str) -> int:
    def is_nice(s: str) -> bool:
        def is_vowel(c: str) -> bool:
            return c in {"a", "e", "i", "o", "u"}

        def is_invalid(c: str) -> bool:
            return c in {"ab", "cd", "pq", "xy"}

        num_vowels = int(is_vowel(s[0]))
        has_consecutive = False
        has_invalid_str = False

        for i in range(1, len(s)):
            num_vowels = num_vowels + int(is_vowel(s[i]))
            has_consecutive = has_consecutive or s[i] == s[i - 1]
            has_invalid_str = has_invalid_str or is_invalid(s[i - 1 : i + 1])

        return num_vowels >= 3 and has_consecutive and not has_invalid_str

    return solve(data, is_nice)


@solution.part_two(year=2015, problem=5)
def part_two(data: str) -> int:
    def is_nice(s: str) -> bool:
        pair_pos = defaultdict(list)
        has_pair_pos = False
        has_repeat = False

        for i in range(len(s) - 1):
            pair_pos[s[i : i + 2]].append(i)
            has_pair_pos = has_pair_pos or (
                pair_pos[s[i : i + 2]][-1] - pair_pos[s[i : i + 2]][0] > 1
            )

        for i in range(len(s) - 2):
            has_repeat = has_repeat or s[i] == s[i + 2]

        return has_pair_pos and has_repeat

    return solve(data, is_nice)
