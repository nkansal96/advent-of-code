from typing import Set, Tuple

from aoc.common import solution


def solve(data: str, instr_filter=lambda i, x: True) -> Set[Tuple[int, int]]:
    pos = (0, 0)
    visited = {pos}

    for i, instr in enumerate(data):
        if not instr_filter(i, instr):
            continue

        dx = -1 if instr == "<" else 1 if instr == ">" else 0
        dy = -1 if instr == "v" else 1 if instr == "^" else 0
        pos = (pos[0] + dx, pos[1] + dy)
        visited.add(pos)

    return visited


@solution.part_one(year=2015, problem=3)
def part_one(data: str) -> int:
    return len(solve(data))


@solution.part_two(year=2015, problem=3)
def part_two(data: str) -> int:
    santa = solve(data, instr_filter=lambda i, x: i % 2 == 0)
    robo_santa = solve(data, instr_filter=lambda i, x: i % 2 == 1)
    return len(santa | robo_santa)
