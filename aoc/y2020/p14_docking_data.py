import re
from typing import Callable, Iterable, List, Tuple

from aoc.common import input
from aoc.common import solution


def parse_line(s: str) -> Tuple:
    m = re.match(r"mask = (.*)", s)
    if m:
        return "mask", m.group(1)

    m = re.match(r"mem\[(\d+)] = (\d+)", s)
    if m:
        return "mem", int(m.group(1)), int(m.group(2))


def compute_val(mask: str, val: int) -> int:
    return sum(
        ((val >> i) & 1) << i if b == "X" else int(b) << i
        for (i, b) in enumerate(mask[::-1])
    )


def expand_address(mask: List[str], i: int = 0, addr: str = "") -> Iterable[int]:
    if len(addr) == len(mask):
        yield int(addr, 2)
    elif mask[i] != "X":
        yield from expand_address(mask, i + 1, addr + str(mask[i]))
    else:
        yield from expand_address(mask, i + 1, addr + "0")
        yield from expand_address(mask, i + 1, addr + "1")


def compute_addresses(mask: str, addr: int) -> Iterable[int]:
    val = []
    for i, m in enumerate(mask[::-1]):
        val.insert(0, (addr >> i) & 1 if m == "0" else m)
    return expand_address(val)


def initialize_and_sum_memory(
    data: input.Tokenized,
    update_regs: Callable[[str, int, int], Iterable[Tuple[int, int]]],
):
    mask, regs = "", {}
    for op, *args in data.each_token_as(parse_line):
        if op == "mask":
            mask = args[0]
        if op == "mem":
            regs.update(dict(update_regs(mask, *args)))
    return sum(regs.values())


@solution.part_one(year=2020, problem=14)
def _(data: input.Tokenized[input.NL]) -> int:
    return initialize_and_sum_memory(
        data, lambda mask, addr, val: [(addr, compute_val(mask, val))]
    )


@solution.part_two(year=2020, problem=14)
def _(data: input.Tokenized[input.NL]) -> int:
    return initialize_and_sum_memory(
        data, lambda mask, a, val: ((addr, val) for addr in compute_addresses(mask, a))
    )
