from typing import List

from aoc.common import solution


def increment_password(password: List[int]) -> List[int]:
    i = len(password) - 1
    password[i] += 1

    while i >= 0 and password[i] > ord("z"):
        password[i] = ord("a")
        password[i - 1] += 1
        i -= 1

    return password


@solution.part_one(year=2015, problem=11)
def part_one(data: str) -> str:
    def is_valid(password: List[int]) -> bool:
        # check for increasing straight
        for i in range(len(password) - 2):
            sl = password[i : i + 3]
            if sl[2] == sl[1] + 1 and sl[1] == sl[0] + 1:
                break
        else:
            return False

        # check for i o l
        if len(set(map(ord, ("i", "o", "l"))) & set(password)) > 0:
            return False

        # check for two pairs of non-overlapping, different conseq same-chars
        i = 0
        last_pair = None
        two_pair = False
        while i < len(password) - 1:
            a, b = password[i : i + 2]
            if a == b and last_pair is None:
                last_pair = a
                i += 1
            if a == b and last_pair is not None and a != last_pair:
                two_pair = True
                i += 1
            i += 1

        return two_pair

    password = increment_password(list(map(ord, data)))
    while not is_valid(password):
        password = increment_password(password)

    return "".join(map(chr, password))


@solution.part_two(year=2015, problem=11)
def part_two(data: str) -> str:
    return part_one(part_one(data))
