import collections
import dataclasses
import math

from typing import *

from aoc.common import input
from aoc.common import solution


@dataclasses.dataclass
class Tile:
    id: int
    grid: List[List[str]]

    @property
    def left(self) -> List[str]:
        return [r[0] for r in self.grid]

    @property
    def right(self) -> List[str]:
        return [r[-1] for r in self.grid]

    @property
    def bottom(self) -> List[str]:
        return self.grid[-1]

    @property
    def top(self) -> List[str]:
        return self.grid[0]

    def rotate_right(self) -> "Tile":
        return Tile(
            self.id,
            [[row[i] for row in reversed(self.grid)] for i in range(len(self.grid))],
        )

    def flip_vertical(self) -> "Tile":
        return Tile(
            self.id,
            [self.grid[len(self.grid) - i - 1] for i in range(len(self.grid))],
        )

    def orientations(self) -> Iterator["Tile"]:
        t = self
        for _ in range(4):
            for _ in range(2):
                yield t
                t = t.flip_vertical()
            t = t.rotate_right()

    def without_border(self):
        return [row[1:-1] for row in self.grid[1:-1]]

    def __repr__(self):
        return f"<Tile id={self.id}>"


def parse_data(data: input.Tokenized) -> List[Tile]:
    tiles: List[Tile] = []
    for t in data:
        lines = t.split("\n")
        tile_id = int(lines[0].split(" ")[1].split(":")[0])
        tiles.append(Tile(tile_id, list(map(list, lines[1:]))))
    return tiles


def find_next_tiles(adj: List[Optional[Tile]], tiles: List[Tile], remain: Set[int]):
    fns = [
        (lambda t, o: t.top == o.bottom),
        (lambda t, o: t.right == o.left),
        (lambda t, o: t.bottom == o.top),
        (lambda t, o: t.left == o.right),
    ]

    for oth in tiles:
        if oth.id not in remain:
            continue
        for oth in oth.orientations():
            for a, fn in zip(adj, fns):
                if isinstance(a, Tile) and not fn(a, oth):
                    break
            else:
                return oth


def solve(tiles: List[Tile]) -> List[List[Tile]]:
    # start with one of the corner tiles (2797, found by finding all tiles that
    # only fit with two others in a corner fashion). Choose any orientation for
    # that tile, and re-orient the whole grid later

    pos: List[List[Optional[Tile]]] = [[None for _ in range(12)] for _ in range(12)]
    start = next(t for t in tiles if t.id == 2797)
    remain = set(t.id for t in tiles) - {2797}

    pos[11][11] = start
    queue = collections.deque([(10, 11), (11, 10)])

    while queue:
        (y, x) = queue.popleft()

        adj = []
        for (yy, xx) in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]:
            if not (0 <= yy < 12 and 0 <= xx < 12):
                adj.append(None)
            else:
                if pos[yy][xx] is None:
                    queue.append((yy, xx))
                adj.append(pos[yy][xx])

        if pos[y][x] is not None:
            continue

        nxt = find_next_tiles(adj, tiles, remain)
        pos[y][x] = nxt
        remain -= {nxt.id}
        print((y, x), "pattern", adj, "filled with", nxt)

    return pos


def matches_pattern(grid, pattern):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if pattern[y][x] != " " and grid[y][x] != "#":
                return False
    return True


def find_monsters(tile, pattern):
    h, w = len(pattern), len(pattern[0])
    pos = set()

    for y in range(0, len(tile) - (h - 1)):
        for x in range(0, len(tile[0]) - (w - 1)):
            grid = [row[x : x + w] for row in tile[y : y + h]]
            if matches_pattern(grid, pattern):
                pos |= {
                    (y + dy, x + dx)
                    for dy in range(h)
                    for dx in range(w)
                    if tile[y + dy][x + dx] == "#" and pattern[dy][dx] == "#"
                }

    return pos


@solution.part_one(year=2020, problem=20)
def _(data: input.Tokenized[input.NLNL]) -> int:
    grid = solve(parse_data(data))
    sol = [grid[0][0], grid[0][-1], grid[-1][0], grid[-1][-1]]
    return math.prod(t.id for t in sol)


@solution.part_two(year=2020, problem=20)
def _(data: input.Tokenized[input.NLNL]) -> int:
    grid = solve(parse_data(data))

    # reorient the grid. this was done based on quick manual inspection,
    # which showed that each tile needed to be rotated 180 degrees
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = grid[y][x].rotate_right().rotate_right()

    all_lines = []
    for row in grid:
        lines = [[] for _ in range(8)]
        for tile in row:
            wb = tile.without_border()
            for i, l in enumerate(wb):
                lines[i].extend(l)
        all_lines.extend(lines)

    big_tile = Tile(0, all_lines)
    pattern = ["                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "]

    all_on = {
        (y, x)
        for y in range(len(big_tile.grid))
        for x in range(len(big_tile.grid[y]))
        if big_tile.grid[y][x] == "#"
    }

    for tile in big_tile.orientations():
        pos = find_monsters(tile.grid, pattern)
        if len(pos) > 0:
            return len(all_on - pos)
