from typing import Dict, List, Tuple

from aoc.common import input
from aoc.common import solution

MFCSAM_OUTPUT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse_aunt(line: str) -> Tuple[str, Dict[str, int]]:
    name, rest = line.split(": ", 1)
    props = rest.split(", ")
    return name, dict((p.split(": ")[0], int(p.split(": ")[1])) for p in props)


@solution.part_one(year=2015, problem=16)
def part_one(data: input.Tokenized["\n"]) -> str:
    aunts = dict(data.each_token_as(parse_aunt))
    filtered_aunts = []
    for aunt, props in aunts.items():
        for prop, val in MFCSAM_OUTPUT.items():
            if prop in props and val != props[prop]:
                break
        else:
            filtered_aunts.append(aunt)

    return filtered_aunts[0]


@solution.part_two(year=2015, problem=16)
def part_two(data: input.Tokenized["\n"]) -> str:
    aunts = dict(data.each_token_as(parse_aunt))
    filtered_aunts = []
    for aunt, props in aunts.items():
        for prop, val in MFCSAM_OUTPUT.items():
            op = lambda x, y: x == y
            if prop in {"cats", "trees"}:
                op = lambda x, y: x < y
            if prop in {"pomeranians", "goldfish"}:
                op = lambda x, y: x > y

            if prop in props and not op(val, props[prop]):
                break
        else:
            filtered_aunts.append(aunt)

    return filtered_aunts[0]
