from dataclasses import dataclass

from aoc.common import input
from aoc.common import solution


@dataclass
class Reindeer:
    name: str
    speed: int
    run_time: int
    rest_time: int


def parse_reindeer(line: str) -> Reindeer:
    parts = line.split(" ")
    return Reindeer(
        name=parts[0],
        speed=int(parts[3]),
        run_time=int(parts[6]),
        rest_time=int(parts[-2]),
    )


@solution.part_one(year=2015, problem=14)
def part_one(data: input.Tokenized["\n"]) -> int:
    reindeer = list(data.each_token_as(parse_reindeer))

    t = 2503
    farthest = (reindeer[0], 0)
    for r in reindeer:
        dist = (r.speed * r.run_time) * (t // (r.run_time + r.rest_time))
        dist += r.speed * min(r.run_time, (t % (r.run_time + r.rest_time)))
        if dist > farthest[1]:
            farthest = (r, dist)

    return farthest[1]


@solution.part_two(year=2015, problem=14)
def part_two(data: input.Tokenized["\n"]) -> int:
    reindeer = list(data.each_token_as(parse_reindeer))
    # (dist, run_time left, rest_time left, points)
    points = {r.name: (0, r.run_time, 0, 0) for r in reindeer}
    t = 2503

    for i in range(t):
        for r in reindeer:
            (dist, run_time_left, rest_time_left, pts) = points[r.name]
            if run_time_left > 0:
                dist += r.speed
                run_time_left -= 1
                if run_time_left == 0:
                    rest_time_left = r.rest_time
            elif rest_time_left > 0:
                rest_time_left -= 1
                if rest_time_left == 0:
                    run_time_left = r.run_time
            points[r.name] = (dist, run_time_left, rest_time_left, pts)

        farthest_dist = max(points.values(), key=lambda x: x[0])[0]
        for r, v in points.items():
            if v[0] == farthest_dist:
                points[r] = (v[0], v[1], v[2], v[3] + 1)

    return max(points.values(), key=lambda x: x[3])[3]
