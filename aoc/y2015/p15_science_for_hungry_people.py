import functools
from dataclasses import dataclass
from typing import List, Dict, Optional, Iterator, Tuple

from aoc.common import input
from aoc.common import solution


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_ingredient(line: str) -> Tuple[str, Ingredient]:
    name, rest = line.split(": ")
    ingredient = Ingredient(name, 0, 0, 0, 0, 0)

    for property_str in rest.split(", "):
        (prop, val) = property_str.split(" ")
        ingredient.__setattr__(prop, int(val))

    return name, ingredient


def iterate_proportions(
    ingredients: List[Ingredient],
    left: int,
    curr: int = 0,
    proportions: Optional[Dict[str, int]] = None,
) -> Iterator[Dict[str, int]]:
    proportions = proportions or {}
    if len(proportions) == len(ingredients):
        yield proportions

    else:
        lower = left if len(ingredients) - len(proportions or {}) == 1 else 0
        for v in range(lower, left + 1):
            proportions = dict(proportions)
            proportions[ingredients[curr].name] = v
            yield from iterate_proportions(ingredients, left - v, curr + 1, proportions)


def compute_score(
    ingredients: Dict[str, Ingredient], proportions: Dict[str, int]
) -> int:
    all_attrs = [
        sum(
            prop * ingredients[name].__getattribute__(attr)
            for (name, prop) in proportions.items()
        )
        for attr in ("capacity", "durability", "flavor", "texture")
    ]
    return functools.reduce(lambda x, y: max(0, x) * max(0, y), all_attrs)


def compute_calories(
    ingredients: Dict[str, Ingredient], proportions: Dict[str, int]
) -> int:
    return max(
        0,
        sum(prop * ingredients[name].calories for (name, prop) in proportions.items()),
    )


@solution.part_one(year=2015, problem=15)
def part_one(data: input.Tokenized["\n"]) -> int:
    ingredients = dict(data.each_token_as(parse_ingredient))
    return max(
        compute_score(ingredients, proportions)
        for proportions in iterate_proportions(list(ingredients.values()), 100)
    )


@solution.part_two(year=2015, problem=15)
def part_one(data: input.Tokenized["\n"]) -> int:
    ingredients = dict(data.each_token_as(parse_ingredient))
    return max(
        compute_score(ingredients, proportions)
        for proportions in iterate_proportions(list(ingredients.values()), 100)
        if compute_calories(ingredients, proportions) == 500
    )
