from typing import List, Tuple

from aoc.common import input
from aoc.common import solution


def parse_op(s: str) -> Tuple[str, int]:
    op, arg = s.split(" ")
    return op, int(arg)


def run_program(ops: List[Tuple[str, int]]) -> Tuple[bool, int]:
    visited = set()
    acc = 0
    i = 0

    while i < len(ops) and i not in visited:
        visited.add(i)
        op, arg = ops[i]
        if op == "acc":
            acc += arg
        if op == "jmp":
            i += arg - 1
        i += 1

    return i not in visited, acc


@solution.part_one(year=2020, problem=8)
def _(data: input.Tokenized[input.NL]) -> int:
    ops = list(data.each_token_as(parse_op))
    _, acc = run_program(ops)
    return acc


@solution.part_two(year=2020, problem=8)
def _(data: input.Tokenized[input.NL]) -> int:
    ops = list(data.each_token_as(parse_op))
    for i, (op, arg) in enumerate(ops):
        if op == "acc":
            continue
        new_ops = list(ops)
        new_ops[i] = (("nop" if op == "jmp" else "jmp"), arg)
        terminates, acc = run_program(new_ops)
        if terminates:
            return acc
