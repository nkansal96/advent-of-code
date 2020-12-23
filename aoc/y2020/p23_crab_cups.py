import dataclasses

from typing import *

from aoc.common import solution


@dataclasses.dataclass
class Node:
    val: int
    prev: Optional["Node"]
    next: Optional["Node"]


def get_dest_cup(current: int, next_cups: List[int], max_cup):
    while True:
        current -= 1
        if current < 1:
            current = max_cup
        if current not in next_cups:
            break
    return current


def take_n(head: Node, n: int):
    for _ in range(n):
        yield head.val
        head = head.next


def splice_from_and_insert_after(curr: Node, insert_after: Node):
    start = curr.next
    last = curr.next.next.next

    curr.next = last.next
    curr.next.prev = curr

    last.next = insert_after.next
    last.next.prev = last

    insert_after.next = start
    insert_after.next.prev = insert_after


def solve(data: str, iterations, max_num=0):
    cups = list(map(int, list(data)))
    val_to_node = {}

    curr = None
    for c in cups + list(range(max(cups) + 1, max_num + 1)):
        curr = Node(c, curr, None)
        val_to_node[c] = curr
        if curr.prev is not None:
            curr.prev.next = curr

    head = val_to_node[cups[0]]
    head.prev = curr
    head.prev.next = head

    max_num = max(val_to_node.keys())
    curr = head

    for _ in range(iterations):
        next_cups = [curr.next.val, curr.next.next.val, curr.next.next.next.val]
        dest_cup = get_dest_cup(curr.val, next_cups, max_num)
        splice_from_and_insert_after(curr, val_to_node[dest_cup])
        curr = curr.next

    return val_to_node


@solution.part_one(year=2020, problem=23)
def _(data: str) -> str:
    val_to_node = solve(data, 100)
    return "".join(map(str, list(take_n(val_to_node[1].next, 8))))


@solution.part_two(year=2020, problem=23)
def _(data: str) -> int:
    val_to_node = solve(data, 10_000_000, 1_000_000)
    return val_to_node[1].next.val * val_to_node[1].next.next.val
