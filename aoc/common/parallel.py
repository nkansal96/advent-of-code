import multiprocessing
import os

from typing import Tuple, Any, Callable, Optional, Iterable


def find_first_shard(
    shards: Iterable[Tuple[Any, ...]],
    fn: Callable[..., Any],
    extra_args: Optional[Tuple[Any, ...]] = (),
    pool_size=os.cpu_count(),
) -> Optional[Any]:
    with multiprocessing.Pool(pool_size) as p:
        futures = [p.apply_async(fn, (*shard, *extra_args)) for shard in shards]
        for future in futures:
            result = future.get()
            if result is not None:
                return result
    return None
