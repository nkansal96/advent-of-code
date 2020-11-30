import hashlib
from typing import Tuple, Callable


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
