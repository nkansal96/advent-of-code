import re

from typing import *

from aoc.common import input
from aoc.common import solution


Food = Tuple[List[str], Set[str]]


def parse_food(line: str) -> Food:
    m = re.match(r"^([\w\s]+) \(contains ([^)]+)\)$", line)
    return m.group(1).split(" "), set(m.group(2).split(", "))


def create_mapping(foods: List[Food]) -> Dict[str, Set[str]]:
    mapping = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in mapping:
                mapping[allergen] = set(ingredients)
            else:
                mapping[allergen] &= set(ingredients)
    return mapping


@solution.part_one(year=2020, problem=21)
def _(data: input.Tokenized[input.NL]) -> int:
    foods = list(data.each_token_as(parse_food))
    mapping = create_mapping(foods)
    possible_ingredients = {i for ing in mapping.values() for i in ing}
    return sum(i not in possible_ingredients for ing, al in foods for i in ing)


@solution.part_two(year=2020, problem=21)
def _(data: input.Tokenized[input.NL]) -> str:
    foods = list(data.each_token_as(parse_food))
    mapping = create_mapping(foods)

    for _ in range(len(mapping)):
        for al, ing in mapping.items():
            for i in ing:
                if not any(i in ing2 for (al2, ing2) in mapping.items() if al2 != al):
                    mapping[al] = {i}

    items_flat = sorted([(al, i) for (al, ing) in mapping.items() for i in ing])
    return ",".join(i for (_, i) in items_flat)
