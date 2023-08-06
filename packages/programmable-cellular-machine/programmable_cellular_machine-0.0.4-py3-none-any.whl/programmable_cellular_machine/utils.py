import time
from typing import Any, Callable

from numba import njit


def time_measurement(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result: Any = func(*args, **kwargs)
        print('--- %s seconds ---' % (time.time() - start_time))
        return result

    return wrapper
