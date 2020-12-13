import math
import itertools
from typing import Tuple

from aoc.common import input
from aoc.common import solution


def parse_input(data: input.Tokenized):
    time, buses = tuple(data)
    return int(time), [int(b) if b.isnumeric() else b for b in buses.split(",")]


def next_bus_in(time: int, bus_interval: int):
    next_bus = bus_interval * (time // bus_interval)
    while next_bus < time:
        next_bus += bus_interval
    return next_bus - time


def chinese_remainder(equations: Tuple[Tuple[int], Tuple[int]]):
    # Takes a (list of remainders, corresponding list of mods) and returns
    # t such that t % m == r for each (r, m) in (remainders, mods)

    def mul_inv(a, b):
        # computes the multiplicative inverse x such that (a * x) % b == 1
        return next(x for x in itertools.count() if (a * x) % b == 1)

    total = 0
    remainders, mods = equations
    prod = math.prod(mods)

    for m, r in zip(mods, remainders):
        p = prod // m
        total += r * mul_inv(p, m) * p

    return total % prod


@solution.part_one(year=2020, problem=13)
def _(data: input.Tokenized[input.NL]) -> int:
    time, buses = parse_input(data)
    return math.prod(min((next_bus_in(time, b), b) for b in buses if b != "x"))


@solution.part_two(year=2020, problem=13)
def _(data: input.Tokenized[input.NL]) -> int:
    time, buses = parse_input(data)
    pos_bus = [(p, b) for (p, b) in enumerate(buses) if b != "x"]

    # each equation is in the form (t + p) % b == 0, where t is unknown. since
    # each pair (bi, bj) for i != j is co-prime, we can solve this with CRT.
    #
    # to use chinese remainder theorem, convert each into an equation of the form
    # t = r % b, where r is the remainder p % b such that p > b

    equations = [((p * b - p) % b, b) for (p, b) in pos_bus]
    print("\n".join(f"t = {remainder} mod {b}" for (remainder, b) in equations))
    return chinese_remainder(tuple(zip(*equations)))
