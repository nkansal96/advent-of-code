import math

from typing import Iterator, Optional

from aoc.common import parallel
from aoc.common import solution


def divisors(n: int) -> Iterator[int]:
    yield 1
    if n != 1:
        yield n
    for k in range(2, math.ceil(math.sqrt(n)) + 1):
        if n % k == 0 and n != k:
            yield k
            if n // k != k:
                yield n // k


def find_in_shard(lower: int, upper: int, target: int) -> Optional[int]:
    for i in range(lower, upper):
        div = list(divisors(i))
        total = 10 * sum(div)
        if total >= target:
            return i
    return None


def find_in_shard_part_two(
    lower: int, upper: int, target: int, max_steps: int
) -> Optional[int]:
    def divisor_within_reach(d: int, i: int) -> bool:
        return d * max_steps >= i

    for i in range(lower, upper):
        div = [d for d in divisors(i) if divisor_within_reach(d, i)]
        total = 11 * sum(div)
        if total >= target:
            return i
    return None


@solution.part_one(year=2015, problem=20)
def part_one(data: int) -> int:
    num_shards = 10
    shard_size = 100000
    shards = [(i * shard_size, (i + 1) * shard_size) for i in range(num_shards)]
    return parallel.find_first_shard(shards, find_in_shard, (data,))


@solution.part_two(year=2015, problem=20)
def part_two(data: int) -> int:
    num_shards = 100
    shard_size = 100000
    shards = [(i * shard_size, (i + 1) * shard_size) for i in range(num_shards)]
    return parallel.find_first_shard(shards, find_in_shard_part_two, (data, 50))
