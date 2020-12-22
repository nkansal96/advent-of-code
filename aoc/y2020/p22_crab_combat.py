import collections

from typing import *

from aoc.common import input
from aoc.common import solution


def parse_decks(data: input.Tokenized) -> Tuple[Tuple[int], Tuple[int]]:
    p1, p2 = tuple(data)
    return tuple(map(int, p1.split("\n")[1:])), tuple(map(int, p2.split("\n")[1:]))


def play_game(p: Tuple[int], q: Tuple[int], recurse=False) -> Tuple[int, int]:
    p = collections.deque(p)
    q = collections.deque(q)
    memo = set()

    while len(p) > 0 and len(q) > 0:
        if (tuple(p), tuple(q)) in memo:
            return 1, 0

        memo.add((tuple(p), tuple(q)))
        pc, qc = p.popleft(), q.popleft()

        if recurse and len(p) >= pc and len(q) >= qc:
            winner, _ = play_game(tuple(p)[:pc], tuple(q)[:qc], recurse)
        else:
            winner = 1 if pc > qc else 2

        if winner == 1:
            p.extend([pc, qc])
        else:
            q.extend([qc, pc])

    winner, w = (1, p) if len(p) > 0 else (2, q)
    score = sum((i + 1) * c for i, c in enumerate(reversed(w)))
    return winner, score


@solution.part_one(year=2020, problem=22)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return play_game(*parse_decks(data))[1]


@solution.part_two(year=2020, problem=22)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return play_game(*parse_decks(data), recurse=True)[1]
