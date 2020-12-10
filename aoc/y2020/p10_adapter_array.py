from collections import Counter
from functools import lru_cache

from typing import List, Tuple

from aoc.common import input
from aoc.common import solution


def parse_data(data: input.Tokenized) -> List[int]:
    items = list(data.each_token_as(int))
    return sorted([0] + items + [max(items) + 3])


@lru_cache()
def count_paths(items: Tuple[int], k: int = 0) -> int:
    return k == len(items) - 1 or sum(
        count_paths(items, k + dk)
        for dk in [1, 2, 3]
        if k + dk < len(items) and items[k + dk] - items[k] <= 3
    )


@solution.part_one(year=2020, problem=10)
def _(data: input.Tokenized[input.NL]) -> int:
    items = parse_data(data)
    diffs = Counter(items[i + 1] - items[i] for i in range(len(items) - 1))
    return diffs[1] * diffs[3]


@solution.part_two(year=2020, problem=10)
def _(data: input.Tokenized[input.NL]) -> int:
    return count_paths(tuple(parse_data(data)))
