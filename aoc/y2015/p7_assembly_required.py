import re

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Union

from aoc.common import input
from aoc.common import solution


@dataclass
class UnaryOp:
    op: str
    arg: str
    output: str

    def var_args(self) -> List[str]:
        return list(filter(lambda arg: not arg.isnumeric(), self.args()))

    def args(self) -> List[str]:
        return [self.arg]

    def __call__(self, x: int) -> int:
        return {"NOT": ~x, None: x}[self.op]


@dataclass
class BinaryOp:
    op: str
    left_arg: str
    right_arg: str
    output: str

    def var_args(self) -> List[str]:
        return list(filter(lambda arg: not arg.isnumeric(), self.args()))

    def args(self) -> List[str]:
        return [self.left_arg, self.right_arg]

    def __call__(self, l: int, r: int) -> int:
        return {
            "AND": l & r,
            "OR": l | r,
            "LSHIFT": l << max(0, r),
            "RSHIFT": l >> max(0, r),
        }[self.op]


Op = Union[UnaryOp, BinaryOp]


def parse_op(line: str) -> Op:
    # parse a unary op:
    m = re.match(r"(?:(\w+) )?([a-z0-9]+) -> ([a-z]+)", line)
    if m:
        return UnaryOp(op=m.group(1), arg=m.group(2), output=m.group(3))

    # parse a binary op:
    m = re.match(r"([a-z0-9]+) ([A-Z]+) ([a-z0-9]+) -> ([a-z]+)", line)
    if m:
        return BinaryOp(
            op=m.group(2),
            left_arg=m.group(1),
            right_arg=m.group(3),
            output=m.group(4),
        )


def build_dependency_graphs(
    ops: List[Op],
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    in_edges = defaultdict(set)
    out_edges = defaultdict(set)

    for op in ops:
        args = op.var_args()
        in_edges[op.output] = in_edges[op.output].union(args)
        for arg in args:
            out_edges[arg] = out_edges[arg].union({op.output})

    return in_edges, out_edges


def solve(ops: List[Op], overrides: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    in_degree, graph = build_dependency_graphs(ops)
    op_map = {op.output: op for op in ops}
    res = dict(overrides or {})

    def resolve(v: str) -> int:
        return int(v) if v.isnumeric() else res[v]

    q = [wire for (wire, d) in in_degree.items() if len(d) == 0]
    while q:
        op = op_map[q.pop()]
        if op.output not in res:
            res[op.output] = op(*list(map(resolve, op.args())))

        for dep_wire in graph[op.output]:
            in_degree[dep_wire] -= {op.output}
            if len(in_degree[dep_wire]) == 0 and dep_wire not in res:
                q.append(dep_wire)

    return res


@solution.part_one(year=2015, problem=7)
def part_one(data: input.Tokenized["\n"]) -> int:
    ops = list(data.each_token_as(parse_op))
    s = solve(ops)
    return s["a"]


@solution.part_two(year=2015, problem=7)
def part_two(data: input.Tokenized["\n"]) -> int:
    ops = list(data.each_token_as(parse_op))
    s = solve(ops, {"b": part_one(data)})
    return s["a"]
