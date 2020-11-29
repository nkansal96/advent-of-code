import re

from aoc.common import input
from aoc.common import solution


@solution.part_one(year=2015, problem=8)
def part_one(data: input.Tokenized["\n"]) -> int:
    total_code = 0
    total_data = 0
    for line in data:
        total_code += len(line)
        total_data += len(re.sub(r"\\\"|\\\\|\\x[a-zA-Z0-9]{2}", ".", line)) - 2
    return total_code - total_data


@solution.part_two(year=2015, problem=8)
def part_two(data: input.Tokenized["\n"]) -> int:
    total_code = 0
    total_encoded = 0
    for line in data:
        total_code += len(line)
        total_encoded += len(line) + line.count("\\") + line.count('"') + 2
    return total_encoded - total_code
