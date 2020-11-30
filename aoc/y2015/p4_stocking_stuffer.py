from aoc.common import solution
from aoc.common import utils


@solution.part_one(year=2015, problem=4)
def part_one(data: str) -> int:
    return utils.iter_md5(
        data, 0, lambda md5: md5[0] == 0 and md5[1] == 0 and md5[2] < 16
    )[0]


@solution.part_two(year=2015, problem=4)
def part_one(data: str) -> int:
    return utils.iter_md5(
        data, 0, lambda md5: md5[0] == 0 and md5[1] == 0 and md5[2] == 0
    )[0]
