import re

from typing import Dict, Tuple, List

from aoc.common import input
from aoc.common import solution


def parse_bag(line: str) -> Tuple[str, List[Tuple[int, str]]]:
    bag, contains = line.split(" bags contain ")
    return bag, [(int(x), y) for (x, y) in re.findall(r"(\d+) ([\w\s]+) bag", contains)]


def contains_bag(bag: str, bags: Dict[str, List[Tuple[int, str]]], target: str) -> bool:
    return bag == target or any(
        contains_bag(b, bags, target) for (_, b) in bags.get(bag, [])
    )


def count_bags(bag: str, bags: Dict[str, List[Tuple[int, str]]]) -> int:
    return sum((n * (1 + count_bags(b, bags)) for (n, b) in bags.get(bag, [])), 0)


@solution.part_one(year=2020, problem=7)
def _(data: input.Tokenized[input.NL]) -> int:
    bags = dict(data.each_token_as(parse_bag))
    return sum(contains_bag(bag, bags, "shiny gold") for bag in bags) - 1


@solution.part_two(year=2020, problem=7)
def _(data: input.Tokenized[input.NL]) -> int:
    return count_bags("shiny gold", dict(data.each_token_as(parse_bag)))
