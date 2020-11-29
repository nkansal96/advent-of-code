from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Iterable

from aoc.common import input
from aoc.common import solution


TURN_OFF = "turn off"
TURN_ON = "turn on"
TOGGLE = "toggle"


@dataclass
class Action:
    action: str
    start: Tuple[int, ...]
    end: Tuple[int, ...]


def parse_action(line: str) -> Action:
    if line.startswith(TURN_OFF) or line.startswith(TURN_ON):
        action = TURN_OFF if line.startswith(TURN_OFF) else TURN_ON
        _, _, start, _, end = line.split(" ")
        return Action(
            action=action,
            start=tuple(map(int, start.split(","))),
            end=tuple(map(int, end.split(","))),
        )

    if line.startswith(TOGGLE):
        _, start, _, end = line.split(" ")
        return Action(
            action=TOGGLE,
            start=tuple(map(int, start.split(","))),
            end=tuple(map(int, end.split(","))),
        )


def solve(
    actions: Iterable[Action], action_map: Dict[str, Callable[[int], int]]
) -> int:
    grid = [[0 for i in range(1000)] for j in range(1000)]

    for action in actions:
        fn = action_map.get(action.action)
        assert (
            fn is not None
        ), f"Could not decode action {action.action} in {action_map}"

        for x in range(action.start[0], action.end[0] + 1):
            for y in range(action.start[1], action.end[1] + 1):
                grid[y][x] = fn(grid[y][x])

    return sum(c for r in grid for c in r)


@solution.part_one(year=2015, problem=6)
def part_one(data: input.Tokenized["\n"]) -> int:
    action_map = {
        TURN_OFF: lambda x: 0,
        TURN_ON: lambda x: 1,
        TOGGLE: lambda x: 1 - x,
    }

    return solve(data.each_token_as(parse_action), action_map)


@solution.part_two(year=2015, problem=6)
def part_one(data: input.Tokenized["\n"]) -> int:
    action_map = {
        TURN_OFF: lambda x: max(0, x - 1),
        TURN_ON: lambda x: x + 1,
        TOGGLE: lambda x: x + 2,
    }

    return solve(data.each_token_as(parse_action), action_map)
