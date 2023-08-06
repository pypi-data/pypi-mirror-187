import abc
from typing import Any, Generator, Iterable

import numpy as np
from numba import njit

from programmable_cellular_machine.hight import hight_load


class BasePlace(abc.ABC):

    width: int
    height: int

    data: dict

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.data = self.make_data()

    def make_layout(self):
        return self.__class__(self.width, self.height)

    @abc.abstractmethod
    def make_data(self) -> Any:
        pass

    @abc.abstractmethod
    def cells(self) -> Iterable[tuple[int, int, int]]:
        pass

    @abc.abstractmethod
    def set(self, pos_x, pos_y, value) -> None:
        pass

    @abc.abstractmethod
    def get(self, pos_x: int, pos_y: int, default: int = 0) -> int:
        pass

    @abc.abstractmethod
    def radius(self, pos_x: int, pos_y: int, width: int):
        pass


class DictPlace(BasePlace):
    """Реализация полотна на основе двумерного python dict"""

    # @profile
    def make_data(self) -> dict:
        data = {}

        for pos_x in range(self.width):
            data[pos_x] = {}
            for pos_y in range(self.height):
                data[pos_x][pos_y] = 0

        return data

    @property
    def cells(self) -> Generator[tuple[int, int, int], None, None]:
        data_list: list[tuple[int, int, int]] = []

        for pos_x, poss_y in self.data.items():
            for pos_y, value in poss_y.items():
                data_list.append((pos_x, pos_y, value))

        return data_list

    def set(self, pos_x, pos_y, value):
        self.data[pos_x][pos_y] = value

    def get(self, pos_x: int, pos_y: int, default: int = 0):
        try:
            return self.data[pos_x][pos_y]

        except KeyError:
            return default

    def radius(self, pos_x: int, pos_y: int, width: int):
        data_list = []

        for inner_pos_x, inner_pos_y in hight_load.get_radius_positions(pos_x, pos_y, width):
            data_list.append((inner_pos_x, inner_pos_y, self.get(inner_pos_x, inner_pos_y)))

        return data_list
