from programmable_cellular_machine.places import BasePlace
import numpy as np
from typing import Generator

import numpy as np

from programmable_cellular_machine.hight import hight_load


class BaseHightPlace(BasePlace):
    """Базовый класс для высоко производительных полотен"""

    data: np.ndarray


class NumpyPlace(BaseHightPlace):
    """Реализация полотна на основе двумерного nympy array"""

    def make_data(self):
        return np.full((self.width, self.height), 0, dtype='int')

    @property
    def cells(self) -> Generator[tuple[int, int, int], None, None]:
        return hight_load.get_cells(self.data)

    def set(self, pos_x, pos_y, value) -> None:
        hight_load.set_in_array(self.data, pos_x, pos_y, value)

    def get(self, pos_x: int, pos_y: int, default: int = 0) -> int:
        return self.data[pos_x, pos_y]

    def radius(self, pos_x: int, pos_y: int, width: int):
        return hight_load.get_radius(self.data, pos_x, pos_y, width)
