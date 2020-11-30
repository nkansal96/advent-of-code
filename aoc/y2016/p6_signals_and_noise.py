from collections import Counter
from typing import List

from aoc.common import input
from aoc.common import solution


def column_counters(data: input.Tokenized) -> List[Counter]:
    data = list(data)
    width = len(data[0])
    columns = [[word[i] for word in data] for i in range(width)]
    return [Counter(col) for col in columns]


@solution.part_one(year=2016, problem=6)
def part_one(data: input.Tokenized["\n"]) -> str:
    counters = column_counters(data)
    return "".join(max(c.items(), key=lambda x: x[1])[0] for c in counters)


@solution.part_two(year=2016, problem=6)
def part_two(data: input.Tokenized["\n"]) -> str:
    counters = column_counters(data)
    return "".join(min(c.items(), key=lambda x: x[1])[0] for c in counters)
