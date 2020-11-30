from aoc.common import solution
from aoc.common import utils


def stop_cond(md5: bytes) -> bool:
    return md5[0] == 0 and md5[1] == 0 and md5[2] < 16


@solution.part_one(year=2016, problem=5)
def part_one(data: str) -> str:
    i = 0
    password = []
    while len(password) < 8:
        i, hash = utils.iter_md5(data, i, stop_cond)
        password.append(hex(hash[2] & 0b1111)[2:])
    return "".join(password)


@solution.part_two(year=2016, problem=5)
def part_two(data: str) -> str:
    i = 0
    password = [0] * 8

    while any(p == 0 for p in password):
        i, hash = utils.iter_md5(data, i, stop_cond)
        pos = hash[2] & 0b1111
        char = (hash[3] >> 4) & 0b1111
        if pos < 8 and password[pos] == 0:
            password[pos] = hex(char)[2:]

    return "".join(map(str, password))
