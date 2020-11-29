import itertools
from typing import Tuple, Iterator

from aoc.common import input
from aoc.common import solution


STORE = {
    "weapons": [
        ("Dagger", 8, 4, 0),
        ("Shortsword", 10, 5, 0),
        ("Warhammer", 25, 6, 0),
        ("Longsword", 40, 7, 0),
        ("Greataxe", 74, 8, 0),
    ],
    "armor": [
        ("Leather", 13, 0, 1),
        ("Chainmail", 31, 0, 2),
        ("Splintmail", 53, 0, 3),
        ("Bandedmail", 75, 0, 4),
        ("Platemail", 102, 0, 5),
    ],
    "rings": [
        ("Damage +1", 25, 1, 0),
        ("Damage +2", 50, 2, 0),
        ("Damage +3", 100, 3, 0),
        ("Defense +1", 20, 0, 1),
        ("Defense +2", 40, 0, 2),
        ("Defense +3", 80, 0, 3),
    ],
}


def store_combinations():
    for weapon in STORE["weapons"]:
        for armor in [None, *STORE["armor"]]:
            for i in range(0, 3):
                for rings in itertools.combinations(STORE["rings"], i):
                    yield weapon, armor, rings


def game_results(data: input.Tokenized["\n"]) -> Iterator[Tuple[int, int, int]]:
    (boss_base_hp, boss_base_damage, boss_base_armor) = data.each_token_as(
        lambda d: int(d.split(": ")[1])
    )

    for (weapon, armor, rings) in store_combinations():
        cost, damage, defense = [
            weapon[i] + (armor[i] if armor else 0) + sum([ring[i] for ring in rings])
            for i in [1, 2, 3]
        ]

        boss_damage = max(1, boss_base_damage - defense)
        player_damage = max(1, damage - boss_base_armor)

        boss_hp = boss_base_hp
        player_hp = 100
        while boss_hp > 0 and player_hp > 0:
            boss_hp -= player_damage
            if boss_hp > 0:
                player_hp -= boss_damage

        yield cost, player_hp, boss_hp


@solution.part_one(year=2015, problem=21)
def part_one(data: input.Tokenized["\n"]) -> int:
    min_cost = 10 ** 10
    for (cost, player_hp, boss_hp) in game_results(data):
        if player_hp > 0 and cost < min_cost:
            min_cost = cost
    return min_cost


@solution.part_two(year=2015, problem=21)
def part_two(data: input.Tokenized["\n"]) -> int:
    max_cost = 0
    for (cost, player_hp, boss_hp) in game_results(data):
        if player_hp <= 0 and cost > max_cost:
            max_cost = cost
    return max_cost
