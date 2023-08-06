import numpy as np
from numba import int32, njit
from numba.core.types import List

# from numba.core.types import List


@njit(cache=True, locals={'inner_pos_x': int32, 'inner_pos_y': int32})
def get_cells(data: np.ndarray) -> list[tuple[int, int, int]]:
    data_list = []
    for (inner_pos_x, inner_pos_y), value in np.ndenumerate(data):
        data_list.append((inner_pos_x, inner_pos_y, value))
    return data_list


@njit(cache=True, locals={'inner_pos_x': int32, 'inner_pos_y': int32})
def get_radius_positions(pos_x: int, pos_y: int, width: int):
    data_list = []

    for inner_pos_x in range(pos_x - width, pos_x + width + 1):
        for inner_pos_y in range(pos_y - width, pos_y + width + 1):
            if inner_pos_x == pos_x and inner_pos_y == pos_y:
                continue

            data_list.append((inner_pos_x, inner_pos_y))

    return data_list


@njit(cache=True, locals={'inner_pos_x': int32, 'inner_pos_y': int32})
def get_radius(data: np.ndarray, pos_x: int, pos_y: int, width: int):
    data_list = []

    for inner_pos_x, inner_pos_y in get_radius_positions(pos_x, pos_y, width):
        data_list.append((inner_pos_x, inner_pos_y, data[inner_pos_x, inner_pos_y]))

    return data_list


@njit(cache=True)
def set_in_array(data: np.ndarray, pos_x: int, pos_y: int, value: int):
    data[pos_x, pos_y] = value


@njit(cache=True, locals={'lives': int32, 'sub_value': int32})
def configurable_rule_implement(
    data: np.ndarray,
    pos_x: int,
    pos_y: int,
    value: int,
    radius: int,
    birth_trigger: list[int],
    survival_trigger: list[int],
):
    lives = 0

    for _, _, sub_value in get_radius(data, pos_x, pos_y, radius):
        lives += sub_value

    # if lives in birth_trigger:
    #     return 1
    for number in birth_trigger:
        if lives == number:
            return 1

    # if value and lives in survival_trigger:
    #     return 1
    if value:
        for number in survival_trigger:
            if lives == number:
                return 1

    return 0
