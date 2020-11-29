from dataclasses import dataclass
from typing import List, Dict

from aoc.common import input
from aoc.common import solution


@dataclass
class Instruction:
    op: str
    reg: str
    offset: int = 0


def parse_instruction(line: str) -> Instruction:
    left, *rest = line.split(", ")
    op, reg = left.split(" ")
    offset = int(rest[0]) if len(rest) > 0 else int(reg) if op == "jmp" else 0
    return Instruction(op=op, reg=reg, offset=offset)


def execute(program: List[Instruction], registers: Dict[str, int]) -> Dict[str, int]:
    i = 0
    while 0 <= i < len(program):
        instr = program[i]
        if instr.op == "hlf":
            registers[instr.reg] /= 2
        if instr.op == "tpl":
            registers[instr.reg] *= 3
        if instr.op == "inc":
            registers[instr.reg] += 1
        if instr.op == "jmp":
            i += instr.offset - 1
        if instr.op == "jie":
            if registers[instr.reg] % 2 == 0:
                i += instr.offset - 1
        if instr.op == "jio":
            if registers[instr.reg] == 1:
                i += instr.offset - 1
        i += 1

    return registers


@solution.part_one(year=2015, problem=23)
def part_one(data: input.Tokenized["\n"]) -> int:
    instructions = list(data.each_token_as(parse_instruction))
    registers = {"a": 0, "b": 0}
    return execute(instructions, registers)["b"]


@solution.part_two(year=2015, problem=23)
def part_two(data: input.Tokenized["\n"]) -> int:
    instructions = list(data.each_token_as(parse_instruction))
    registers = {"a": 1, "b": 0}
    return execute(instructions, registers)["b"]
