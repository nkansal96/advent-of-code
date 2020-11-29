import json
from typing import Any

from aoc.common import input
from aoc.common import solution


def recursive_sum(data: Any, filter_fn=lambda x: True) -> int:
    if not filter_fn(data):
        return 0
    if isinstance(data, (int, float)):
        return data
    if isinstance(data, list):
        return sum(recursive_sum(d, filter_fn) for d in data)
    if isinstance(data, dict):
        return sum(recursive_sum(d, filter_fn) for d in data.values())
    return 0


@solution.part_one(year=2015, problem=12)
def part_one(data: input.JSON) -> int:
    return recursive_sum(data)


@solution.part_two(year=2015, problem=12)
def part_two(data: input.JSON) -> int:
    return recursive_sum(
        data,
        filter_fn=lambda obj: not isinstance(obj, dict) or "red" not in obj.values(),
    )
