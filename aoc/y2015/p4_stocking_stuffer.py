import hashlib

from aoc.common import solution


def solve(data: str, stop_cond=lambda md5: True) -> int:
    i = 0
    md5 = bytes()
    while len(md5) == 0 or not stop_cond(md5):
        i += 1
        md5 = hashlib.md5(bytes(data + str(i), "utf-8")).digest()
    return i


@solution.part_one(year=2015, problem=4)
def part_one(data: str) -> int:
    return solve(data, lambda md5: md5[0] == 0 and md5[1] == 0 and md5[2] < 16)


@solution.part_two(year=2015, problem=4)
def part_one(data: str) -> int:
    return solve(data, lambda md5: md5[0] == 0 and md5[1] == 0 and md5[2] == 0)
