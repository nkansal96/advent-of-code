import collections
import typing

from aoc.common import input
from aoc.common import solution


def has_sum(counts: typing.Counter[int], target: int) -> bool:
    for i in counts:
        j = target - i
        if j in counts:
            if j == i and counts.get(j, 0) < 2:
                continue
            return True


@solution.part_one(year=2020, problem=9)
def part_one(data: input.Tokenized[input.NL]) -> int:
    items = list(data.each_token_as(int))
    window = 25
    counts = collections.Counter(items[:window])

    for i in range(window, len(items)):
        if not has_sum(counts, items[i]):
            return items[i]
        counts.update({items[i - window]: -1, items[i]: 1})


@solution.part_two(year=2020, problem=9)
def _(data: input.Tokenized[input.NL]) -> int:
    target = part_one(data)
    items = list(data.each_token_as(int))
    lower, upper, total = 0, 0, 0

    while upper < len(items):
        if total == target:
            nums = items[lower:upper]
            return max(nums) + min(nums)
        if total < target:
            total += items[upper]
            upper += 1
        if total > target:
            total -= items[lower]
            lower += 1
