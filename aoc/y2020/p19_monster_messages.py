import itertools
import re

from aoc.common import input
from aoc.common import solution
from aoc.common import utils


def parse_data(data):
    raw_rules, raw_messages = tuple(data)
    rules = {}
    derivations = {}
    for r in raw_rules.split("\n"):
        m = re.match(r"^(\d+): \"(\w+)\"$", r)
        if m:
            derivations[m.group(1)] = m.group(2)
        else:
            rule_id, rule_expr = r.split(": ")
            rules[rule_id] = [tuple(rule.split(" ")) for rule in rule_expr.split(" | ")]

    return rules, derivations, set(raw_messages.split("\n"))


def resolve_rule(rules, start, memo):
    messages = set()
    if start in memo:
        return memo[start]

    for r in rules[start]:
        sub_rules = (resolve_rule(rules, p, memo) for p in r)
        messages |= set(map(utils.concat, itertools.product(*sub_rules)))

    memo[start] = messages
    return messages


def expand_rule(rules, start, derive, msg):
    if msg in derive[start]:
        return True

    # If the message isn't in a pre-derived list of existing rules, try to dynamically
    # expand it using the rule 0 => 8 11 by finding msg = ab such that 8 derives a and
    # 11 derives b.
    if start == "0":
        step = min(map(len, derive["8"]))
        for i in range(step, len(msg) - 1, step):
            a, b = msg[:i], msg[i:]
            if expand_rule(rules, "8", derive, a) & expand_rule(rules, "11", derive, b):
                return True

    # 8 => 42 | 42 8  - translates to 42+ in regex terms
    if start == "8":
        while True:
            for w in derive["42"]:
                if msg.startswith(w):
                    msg = msg[len(w) :]
                    if len(msg) == 0:
                        return True
                    break
            else:
                break

    # 11 => 42 31 | 42 11 31  - translate to 42{n}31{n} in regex terms
    if start == "11":
        while True:
            for w, v in itertools.product(derive["42"], derive["31"]):
                if msg.startswith(w) and msg.endswith(v):
                    msg = msg[len(w) : -len(v)]
                    if len(msg) == 0:
                        return True
                    break
            else:
                break

    return False


@solution.part_one(year=2020, problem=19)
def _(data: input.Tokenized[input.NLNL]) -> int:
    rules, derivations, messages = parse_data(data)
    valid_messages = resolve_rule(rules, "0", derivations)
    return len(messages & valid_messages)


@solution.part_two(year=2020, problem=19)
def _(data: input.Tokenized[input.NLNL]) -> int:
    rules, derivations, messages = parse_data(data)
    resolve_rule(rules, "0", derivations)
    return sum(expand_rule(rules, "0", derivations, m) for m in messages)
