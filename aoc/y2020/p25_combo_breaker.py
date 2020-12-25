import functools

from aoc.common import input
from aoc.common import solution


def decrypt(key: int) -> int:
    i, val = 0, 1
    while val != key:
        val = (val * 7) % 20201227
        i += 1
    return i


@solution.part_one(year=2020, problem=25)
def _(data: input.Tokenized[input.NL]) -> int:
    pub_a, pub_b = map(int, data)
    return functools.reduce(lambda v, _: v * pub_a % 20201227, range(decrypt(pub_b)), 1)
