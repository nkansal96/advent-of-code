from typing import List, Tuple

from aoc.common import input
from aoc.common import solution


def count_combinations(
    containers: List[int], target: int, limit: int = -1, curr: int = 0
) -> int:
    if target == 0:
        return 1
    if target < 0 or limit == 0 or curr >= len(containers):
        return 0

    return count_combinations(containers, target, limit, curr + 1) + count_combinations(
        containers, target - containers[curr], limit - 1, curr + 1
    )


def min_containers(
    containers: List[int], target: int, num_containers: int = 0, curr: int = 0
) -> int:
    if target == 0:
        return num_containers
    if target < 0 or curr >= len(containers):
        return 10 ** 10

    return min(
        min_containers(containers, target, num_containers, curr + 1),
        min_containers(
            containers, target - containers[curr], num_containers + 1, curr + 1
        ),
    )


@solution.part_one(year=2015, problem=17)
def part_one(data: input.Tokenized["\n"]) -> int:
    containers = sorted(data.each_token_as(int))
    return count_combinations(containers, 150)


@solution.part_two(year=2015, problem=17)
def part_two(data: input.Tokenized["\n"]) -> int:
    containers = sorted(data.each_token_as(int))
    num_required = min_containers(containers, 150)
    return count_combinations(containers, 150, num_required)
