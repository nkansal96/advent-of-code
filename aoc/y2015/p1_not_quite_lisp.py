from aoc.common import solution


@solution.part_one(year=2015, problem=1)
def part_one(data: str) -> int:
    return data.count("(") - data.count(")")


@solution.part_two(year=2015, problem=1)
def part_two(data: str) -> int:
    floor = 0
    for i, c in enumerate(data):
        if c == "(":
            floor += 1
        if c == ")":
            floor -= 1
        if floor < 0:
            return i + 1
    return len(data)
