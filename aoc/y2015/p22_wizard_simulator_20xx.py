import copy
from dataclasses import dataclass
from typing import Tuple, List, Iterator, Callable

from aoc.common import input
from aoc.common import solution


@dataclass
class Spell:
    name: str
    cost: int
    turns: int = 0
    damage: int = 0
    armor_increase: int = 0
    mana_increase: int = 0
    hp_increase: int = 0


@dataclass
class GameState:
    player_hp: int
    player_mana: int
    boss_hp: int
    boss_damage: int
    active_spells: List[Spell]


SPELLS = [
    Spell(
        name="Magic Missle",
        cost=53,
        damage=4,
    ),
    Spell(
        name="Drain",
        cost=73,
        damage=2,
        hp_increase=2,
    ),
    Spell(
        name="Shield",
        cost=113,
        turns=6,
        armor_increase=7,
    ),
    Spell(
        name="Poison",
        cost=173,
        turns=6,
        damage=3,
    ),
    Spell(
        name="Recharge",
        cost=229,
        turns=5,
        mana_increase=101,
    ),
]


def play_games(
    state: GameState,
    get_min_cost: Callable[[], int],
    part_two: bool,
    curr_cost: int = 0,
    player_turn: bool = True,
) -> Iterator[Tuple[bool, int]]:
    if state.player_hp > 0 and state.boss_hp <= 0:
        yield True, curr_cost
    elif state.player_hp <= 0 and state.boss_hp > 0:
        yield False, curr_cost
    elif state.player_mana <= 0:
        yield False, curr_cost
    elif curr_cost > get_min_cost():
        yield False, curr_cost
    else:
        armor = 0
        for spell in state.active_spells:
            armor += spell.armor_increase
            state.boss_hp -= spell.damage
            state.player_mana += spell.mana_increase
            spell.turns -= 1

        state.active_spells = [
            spell for spell in state.active_spells if spell.turns > 0
        ]

        if not player_turn:
            new_state = copy.deepcopy(state)
            if new_state.boss_hp > 0:
                new_state.player_hp -= max(1, new_state.boss_damage - armor)
            yield from play_games(new_state, get_min_cost, part_two, curr_cost, True)
            return

        if part_two:
            state.player_hp -= 1
            if state.player_hp <= 0:
                yield False, curr_cost
                return

        for spell in SPELLS:
            if spell.name not in {s.name for s in state.active_spells}:
                new_state = copy.deepcopy(state)
                new_state.player_mana -= spell.cost

                if spell.turns == 0:
                    new_state.boss_hp -= spell.damage
                    new_state.player_hp += spell.hp_increase
                else:
                    new_state.active_spells.append(copy.deepcopy(spell))

                yield from play_games(
                    new_state, get_min_cost, part_two, curr_cost + spell.cost, False
                )


def solve(data: input.Tokenized["\n"], part_two: bool) -> int:
    boss_hp, boss_damage = data.each_token_as(lambda d: int(d.split(": ")[1]))
    initial_state = GameState(
        player_hp=50,
        player_mana=500,
        boss_hp=boss_hp,
        boss_damage=boss_damage,
        active_spells=[],
    )
    min_cost = 10 ** 10
    get_min_cost = lambda: min_cost
    for (won, cost) in play_games(initial_state, get_min_cost, part_two):
        if won and cost < min_cost:
            min_cost = cost
    return min_cost


@solution.part_one(year=2015, problem=22)
def part_one(data: input.Tokenized["\n"]) -> int:
    return solve(data, False)


@solution.part_two(year=2015, problem=22)
def part_two(data: input.Tokenized["\n"]) -> int:
    return solve(data, True)
