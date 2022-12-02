import collections
import functools
import itertools
import math
import operator
import re

from typing import *

from aoc.common import input
from aoc.common import solution

v = {'X': 1, 'Y': 2, 'Z': 3} # move value X = rock, Y = paper, Z = scissor

win_move = {'X': 'C', 'Y': 'A', 'Z': 'B'}
draw_move = {'X': 'A', 'Y': 'B', 'Z': 'C'}
loss_move = {'X': 'B', 'Y': 'C', 'Z': 'A'}

inverted_win_move = dict((v, k) for k, v in win_move.items())
inverted_draw_move = dict((v, k) for k, v in draw_move.items())
inverted_loss_move = dict((v, k) for k, v in loss_move.items())

def score(move) -> int:
    elf, you = move
    win = elf == win_move[you]
    draw = elf == draw_move[you]
    loss = not win and not draw

    return v[you] + (0 if loss else 3 if draw else 6 if win else 0)

@solution.part_one(year=2022, problem=2)
def _(data: input.Tokenized[input.NL]) -> int:
    moves = data.each_token_as(lambda s: s.split(' '))
    return sum(map(score, moves))


@solution.part_two(year=2022, problem=2)
def _(data: input.Tokenized[input.NL]) -> int:
    moves = data.each_token_as(lambda s: s.split(' '))
    move_map = { 'X': inverted_loss_move, 'Y': inverted_draw_move, 'Z': inverted_win_move }
    return sum(
        score((elf, move_map[desired_outcome][elf]))
        for (elf, desired_outcome) in moves
    )
