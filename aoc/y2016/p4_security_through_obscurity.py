import re

from collections import Counter

from aoc.common import input
from aoc.common import solution


def decrypt_room_name(room: str, sector: int) -> str:
    return "-".join(
        "".join(chr((ord(c) - ord("a") + sector) % 26 + ord("a")) for c in part)
        for part in room.split("-")
    )


def room_matches_checksum(room: str, checksum: str) -> bool:
    chars = [
        x[0]
        for x in sorted(
            Counter(room.replace("-", "")).items(),
            key=lambda x: (x[1], -ord(x[0])),
            reverse=True,
        )[: len(checksum)]
    ]
    return "".join(chars) == checksum


@solution.part_one(year=2016, problem=4)
def part_one(data: input.Tokenized["\n"]) -> int:
    matches = data.each_token_as(lambda d: re.match(r"([a-z\-]+)(\d+)\[(\w+)]", d))
    return sum(
        int(sector)
        for name, sector, checksum in map(lambda m: m.groups(), matches)
        if room_matches_checksum(name, checksum)
    )


@solution.part_two(year=2016, problem=4)
def part_two(data: input.Tokenized["\n"]) -> int:
    matches = data.each_token_as(lambda d: re.match(r"([a-z\-]+)(\d+)\[(\w+)]", d))
    decrypted = [
        (decrypt_room_name(name, int(sector)), int(sector))
        for name, sector, checksum in map(lambda m: m.groups(), matches)
    ]
    return [sector for (name, sector) in decrypted if "north" in name][0]
