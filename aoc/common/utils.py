import hashlib
from typing import Any, Callable, Tuple


def sign(x: int) -> int:
    """ Return the sign of a number """
    return -1 if x < 0 else 1


def iter_md5(
    data: str, i: int = 0, stop_cond: Callable[[bytes], bool] = lambda md5: True
) -> Tuple[int, bytes]:
    """ Generate the md5 of strings in the form {data}{i} until stop_cond(md5) is True """
    md5 = bytes()
    while len(md5) == 0 or not stop_cond(md5):
        i += 1
        md5 = hashlib.md5(bytes(data + str(i), "utf-8")).digest()
    return i, md5


def rindex(lst, item):
    """
    Find first place item occurs in list, but starting at end of list.
    Return index of item in list, or -1 if item not found in the list.
    """
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] == item:
            return i
    return -1


def concat(lst, default=""):
    for i in lst:
        default += i
    return default


def is_iterable(data: Any) -> bool:
    try:
        iter(data)
        return True
    except TypeError:
        return False


def hash_(data: Any) -> int:
    """ Intelligently hashes arbitrary data """
    if isinstance(data, dict):
        return hash(tuple(map(hash_, data.items())))
    if is_iterable(data):
        return hash(tuple(map(hash_, data)))
    return hash(data)
