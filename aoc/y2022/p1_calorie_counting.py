import collections
import functools
import itertools
import math
import operator
import re

from typing import *

from aoc.common import input
from aoc.common import solution


@solution.part_one(year=2022, problem=1)
def _(data: input.Tokenized[input.NLNL]) -> int:
    elves = data.each_token_as(lambda elf: [int(x) for x in elf.split('\n')])
    return sum(max(elves, key=lambda x: sum(x)))


@solution.part_two(year=2022, problem=1)
def _(data: input.Tokenized[input.NLNL]) -> int:
    elves = data.each_token_as(lambda elf: [int(x) for x in elf.split('\n')])
    s = list(sorted(elves, key=lambda x: sum(x), reverse=True))
    return sum(sum(x) for x in s[:3])
