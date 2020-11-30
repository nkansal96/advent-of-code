import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple, Union

from aoc.common import input
from aoc.common import solution


@dataclass
class ValueInstruction:
    value: int
    bot: int


@dataclass
class BotInstruction:
    bot: int
    low: Tuple[str, int]
    high: Tuple[str, int]


Instruction = Union[ValueInstruction, BotInstruction]


def parse_instruction(line: str) -> Instruction:
    m = re.match(r"value (\d+) goes to bot (\d+)", line)
    if m:
        return ValueInstruction(*map(int, m.groups()))

    m = re.match(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)", line)
    if m:
        bot = int(m.group(1))
        low = (m.group(2), int(m.group(3)))
        high = (m.group(4), int(m.group(5)))
        return BotInstruction(bot, low, high)


@solution.part_one(year=2016, problem=10)
def part_one(data: input.Tokenized["\n"]) -> int:
    instructions = list(data.each_token_as(parse_instruction))
    outputs = {"output": defaultdict(set), "bot": defaultdict(set)}

    # initialize bots
    for instr in instructions:
        if isinstance(instr, ValueInstruction):
            outputs["bot"][instr.bot].add(instr.value)

    while True:
        for instr in instructions:
            if not isinstance(instr, BotInstruction):
                continue
            if len(outputs["bot"][instr.bot]) != 2:
                continue
            if {17, 61} & outputs["bot"][instr.bot] == {17, 61}:
                return instr.bot

            # give the inputs
            outputs[instr.low[0]][instr.low[1]].add(min(outputs["bot"][instr.bot]))
            outputs[instr.high[0]][instr.high[1]].add(max(outputs["bot"][instr.bot]))

            # remove from current bot
            outputs["bot"][instr.bot].remove(min(outputs["bot"][instr.bot]))
            outputs["bot"][instr.bot].remove(max(outputs["bot"][instr.bot]))


@solution.part_two(year=2016, problem=10)
def part_two(data: input.Tokenized["\n"]) -> int:
    instructions = list(data.each_token_as(parse_instruction))
    outputs = {"output": defaultdict(set), "bot": defaultdict(set)}

    # initialize bots
    for instr in instructions:
        if isinstance(instr, ValueInstruction):
            outputs["bot"][instr.bot].add(instr.value)

    assigned = True

    while assigned:
        assigned = False
        for instr in instructions:
            if not isinstance(instr, BotInstruction):
                continue
            if len(outputs["bot"][instr.bot]) != 2:
                continue

            # give the inputs
            outputs[instr.low[0]][instr.low[1]].add(min(outputs["bot"][instr.bot]))
            outputs[instr.high[0]][instr.high[1]].add(max(outputs["bot"][instr.bot]))

            # remove from current bot
            outputs["bot"][instr.bot].remove(min(outputs["bot"][instr.bot]))
            outputs["bot"][instr.bot].remove(max(outputs["bot"][instr.bot]))

            assigned = True

    return (
        list(outputs["output"][0])[0]
        * list(outputs["output"][1])[0]
        * list(outputs["output"][2])[0]
    )
