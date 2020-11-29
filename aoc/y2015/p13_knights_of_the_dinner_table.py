import itertools

from collections import defaultdict
from typing import Dict, List, Iterator, Tuple

from aoc.common import solution


def parse_input(data: str) -> Dict[str, Dict[str, int]]:
    d = defaultdict(lambda: defaultdict(int))

    for line in data.split("\n"):
        parts = line.split(" ")
        first_person = parts[0]
        gain_or_lose = -1 if parts[2] == "lose" else 1
        happiness_pts = int(parts[3])
        second_person = parts[-1].rstrip(".")
        d[first_person][second_person] = gain_or_lose * happiness_pts

    return d


def generate_arrangements(people: List[str]) -> Iterator[Tuple[str]]:
    return itertools.permutations(people, len(people))


def compute_happiness(arrangement: Tuple[str], table: Dict[str, Dict[str, int]]) -> int:
    happiness = 0
    for i, person in enumerate(arrangement):
        happiness += table[person][arrangement[i - 1]]
        happiness += table[person][arrangement[(i + 1) % len(arrangement)]]
    return happiness


@solution.part_one(year=2015, problem=13)
def part_one(data: str) -> int:
    table = parse_input(data)
    people = list(table.keys())
    return max(
        compute_happiness(arrangement, table)
        for arrangement in generate_arrangements(people)
    )


@solution.part_two(year=2015, problem=13)
def part_two(data: str) -> int:
    table = parse_input(data)
    people = list(table.keys()) + ["me"]
    return max(
        compute_happiness(arrangement, table)
        for arrangement in generate_arrangements(people)
    )
