from aoc.common import solution


def count_and_say(data: str) -> str:
    last_char = data[0]
    num_repeat = 1
    next_data = []
    for c in data[1:]:
        if c != last_char:
            next_data.extend([num_repeat, last_char])
            last_char = c
            num_repeat = 1
        else:
            num_repeat += 1

    next_data.extend([num_repeat, last_char])
    return "".join(map(str, next_data))


def count_n_times(data: str, n: int) -> str:
    while n > 0:
        data = count_and_say(data)
        n -= 1
    return data


@solution.part_one(year=2015, problem=10)
def part_one(data: str) -> int:
    return len(count_n_times(data, 40))


@solution.part_two(year=2015, problem=10)
def part_two(data: str) -> int:
    return len(count_n_times(data, 50))
