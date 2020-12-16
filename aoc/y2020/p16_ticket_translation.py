import math
import re

from typing import Any, List, Tuple

from aoc.common import input
from aoc.common import solution


def parse_data(
    data: input.Tokenized,
) -> Tuple[List[Tuple[Any, ...]], Tuple[int], List[Tuple[int]]]:
    raw_rules, raw_my_ticket, raw_tickets = list(data)

    rules = [
        (m.group(1), *(int(m.group(i)) for i in [2, 3, 4, 5]))
        for m in re.finditer(r"^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$", raw_rules, re.M)
    ]
    my_ticket = tuple(map(int, raw_my_ticket.split(",")))
    tickets = [tuple(map(int, t.split(","))) for t in raw_tickets.split("\n")]

    return rules, my_ticket, tickets


def invalid_cols(ticket: Tuple[int], rules: List[Tuple[int, ...]]):
    for col in ticket:
        if not any(r[1] <= col <= r[2] or r[3] <= col <= r[4] for r in rules):
            yield col


def get_possible_cols(col: List[int], rules: List[Tuple[int, ...]]):
    for r in rules:
        if all(r[1] <= v <= r[2] or r[3] <= v <= r[4] for v in col):
            yield r[0]


@solution.part_one(year=2020, problem=16)
def _(data: input.Tokenized[input.NLNL]) -> int:
    rules, _, tickets = parse_data(data)
    return sum(sum(invalid_cols(t, rules)) for t in tickets)


@solution.part_two(year=2020, problem=16)
def _(data: input.Tokenized[input.NLNL]) -> int:
    rules, my_ticket, tickets = parse_data(data)
    valid_tickets = [t for t in tickets if sum(invalid_cols(t, rules)) == 0]

    match_cols = [
        set(get_possible_cols([t[i] for t in valid_tickets], rules))
        for i in range(len(my_ticket))
    ]

    for _ in range(len(match_cols)):
        for i, cols in enumerate(match_cols):
            if len(cols) == 1:
                for j in range(len(match_cols)):
                    if i != j:
                        match_cols[j] -= cols

    return math.prod(
        t
        for (t, cols) in zip(my_ticket, match_cols)
        if list(cols)[0].startswith("departure")
    )
