from typing import Tuple, List, Iterator

from aoc.common import solution


Rule = Tuple[str, str]


def parse_input(data: str) -> Tuple[List[Rule], str]:
    rule_lines, molecule = data.strip().split("\n\n")
    rules = []
    for rule_line in rule_lines.split("\n"):
        rule_from, rule_to = rule_line.split(" => ")
        rules.append((rule_from, rule_to))

    return rules, molecule


def apply_rule_seq(molecule: str, rule: Rule) -> Iterator[str]:
    rule_from, rule_to = rule
    if rule_from not in molecule:
        return

    parts = molecule.split(rule_from)
    for i in range(1, len(parts)):
        yield rule_from.join(parts[:i]) + rule_to + rule_from.join(parts[i:])


def transform(start_molecule: str, target_molecule: str, rules: List[Rule]) -> int:
    results = {start_molecule}
    next_results = set()
    cost = 0
    while target_molecule not in results:
        cost += 1
        print(cost, len(results))
        for molecule in results:
            for rule in rules:
                for candidate_molecule in apply_rule_seq(molecule, rule):
                    if candidate_molecule not in next_results:
                        next_results.add(candidate_molecule)
        results = next_results
        next_results = set()

    return cost


@solution.part_one(year=2015, problem=19)
def part_one(data: str) -> int:
    rules, molecule = parse_input(data)
    return len(set(res for rule in rules for res in apply_rule_seq(molecule, rule)))


@solution.part_two(year=2015, problem=19)
def part_two(data: str) -> int:
    rules, molecule = parse_input(data)
    return transform("e", molecule, rules)
