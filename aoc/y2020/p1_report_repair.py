from collections import Counter

from aoc.common import input
from aoc.common import solution


@solution.part_one(year=2020, problem=1)
def _(data: input.Tokenized[input.NL]) -> int:
    items = data.each_token_as(int)
    counts = Counter(items)

    for i in items:
        j = 2020 - i
        if j in counts:
            if j == i and counts.get(j, 0) < 2:
                continue
            return i * j


@solution.part_two(year=2020, problem=1)
def _(data: input.Tokenized[input.NL]) -> int:
    items = list(data.each_token_as(int))
    counts = Counter(items)

    for i in range(0, len(items) - 1):
        for j in range(i + 1, len(items)):
            third = 2020 - (items[i] + items[j])
            if third in counts:
                if third == (items[i] + items[j]) and counts.get(third, 0) < 2:
                    continue
                return third * items[i] * items[j]
