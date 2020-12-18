from aoc.common import input
from aoc.common import solution
from aoc.common import utils


def eval_left_to_right(expr) -> int:
    total = expr[0]
    for i in range(1, len(expr)):
        if expr[i] == "+":
            total += expr[i + 1]
        if expr[i] == "*":
            total *= expr[i + 1]
    return total


def eval_add_then_mul(expr) -> int:
    s = [expr[0]]
    for i in range(1, len(expr)):
        if expr[i] == "+":
            s.append(s.pop() + expr[i + 1])
        if expr[i] == "*":
            s.extend(expr[i : i + 2])
    return eval_left_to_right(s)


def compute(expr, sub_expr_evaluator):
    s = []
    for c in expr:
        if c == ")":
            idx = utils.rindex(s, "(")
            s = s[:idx] + [sub_expr_evaluator(s[idx + 1 :])]
        else:
            s.append(int(c) if c.isnumeric() else c)
    return sub_expr_evaluator(s)


@solution.part_one(year=2020, problem=18)
def _(data: input.Tokenized[input.NL]) -> int:
    return sum(compute(expr.replace(" ", ""), eval_left_to_right) for expr in data)


@solution.part_two(year=2020, problem=18)
def _(data: input.Tokenized[input.NL]) -> int:
    return sum(compute(expr.replace(" ", ""), eval_add_then_mul) for expr in data)
