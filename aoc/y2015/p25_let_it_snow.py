from aoc.common import input
from aoc.common import solution


@solution.part_one(year=2015, problem=25)
def part_one(data: input.Tokenized["\n"]) -> int:
    target_row, target_col = data.each_token_as(int)
    # how many codes must we generate before we get to (target_row, target_col)?
    row, col = 1, 1
    max_row = 1
    curr = 20151125

    while row != target_row or col != target_col:
        curr = (curr * 252533) % 33554393
        if row == 1:
            max_row += 1
            row = max_row
            col = 1
        else:
            row -= 1
            col += 1

    return curr


@solution.part_two(year=2015, problem=25)
def part_two(data: input.Tokenized["\n"]) -> int:
    target_row, target_col = data.each_token_as(int)
    return 0
