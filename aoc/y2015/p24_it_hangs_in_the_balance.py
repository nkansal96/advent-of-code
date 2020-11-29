import functools
import itertools
from typing import List, Tuple, Optional, Iterator

from aoc.common import input
from aoc.common import parallel
from aoc.common import solution


def set_sizes(max_size: int, parts: int, prev: int = 1) -> Iterator[Tuple[int, ...]]:
    if parts == 1 and prev <= max_size:
        yield [max_size]
        return
    for i in range(prev, max_size):
        for rest in set_sizes(max_size - i, parts - 1, prev=i):
            yield [i, *rest]


def all_partitions(
    all_items: List[int], parts: int, target_sum: int
) -> Iterator[Tuple[List[int], ...]]:
    def partitions(
        items: List[int], part_sizes: Tuple[int]
    ) -> Iterator[Tuple[List[int], ...]]:
        for k in itertools.combinations(items, part_sizes[0]):
            if sum(k) != target_sum:
                continue
            if len(part_sizes) > 1:
                for rest in partitions(list(set(items) - set(k)), part_sizes[1:]):
                    yield k, *rest
            else:
                yield k,

    for sizes in set_sizes(len(all_items), parts):
        yield from partitions(all_items, sizes)


def optimal_solution(i: int, items: List[int], parts: int) -> Optional[int]:
    target_sum = sum(items) // parts

    min_qe = None
    for first_set in itertools.combinations(items, i):
        if sum(first_set) != target_sum:
            continue

        qe = functools.reduce(lambda x, y: x * y, first_set, 1)
        remaining = list(set(items) - set(first_set))

        for sets in all_partitions(remaining, parts - 1, target_sum):
            if all(sum(s) == target_sum for s in sets):
                if min_qe is None or qe < min_qe:
                    min_qe = qe

    return min_qe


@solution.part_one(year=2015, problem=24)
def part_one(data: input.Tokenized["\n"]) -> int:
    items = list(data.each_token_as(int))
    shards = [(i,) for i in range(len(items) - 2)]
    return parallel.find_first_shard(shards, optimal_solution, (items, 3))


@solution.part_two(year=2015, problem=24)
def part_two(data: input.Tokenized["\n"]) -> int:
    items = list(data.each_token_as(int))
    shards = [(i,) for i in range(len(items) - 3)]
    return parallel.find_first_shard(shards, optimal_solution, (items, 4))
