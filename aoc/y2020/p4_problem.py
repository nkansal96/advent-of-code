import re

from aoc.common import input
from aoc.common import solution


validators = {
    "byr": lambda f: re.match(r"^\d{4}$", f) and 1920 <= int(f) <= 2002,
    "iyr": lambda f: re.match(r"^20(1\d|20)$", f),
    "eyr": lambda f: re.match(r"^20(2\d|30)$", f),
    "hcl": lambda f: re.match(r"^#[0-9a-f]{6}$", f),
    "ecl": lambda f: f in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "hgt": lambda f: re.match(r"^\d+(cm|in)$", f)
    and (
        (f.endswith("cm") and 150 <= int(f[:-2]) <= 193)
        or (f.endswith("in") and 59 <= int(f[:-2]) <= 76)
    ),
    "pid": lambda f: re.match(r"^\d{9}$", f),
}


def parse_passport(passport: str) -> dict:
    return dict(re.findall(r"(\w+):([^\s]+)", passport))


@solution.part_one(year=2020, problem=4)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return sum(
        set(passport.keys()) - {"cid"} == set(validators.keys())
        for passport in data.each_token_as(parse_passport)
    )


@solution.part_two(year=2020, problem=4)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return sum(
        all(
            k in passport and validator(passport[k])
            for (k, validator) in validators.items()
        )
        for passport in data.each_token_as(parse_passport)
    )
