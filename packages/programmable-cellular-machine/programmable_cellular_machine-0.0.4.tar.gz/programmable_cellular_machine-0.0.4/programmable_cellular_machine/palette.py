import math
import time
from typing import Tuple


def gen_rgb() -> dict:
    data = {}

    index = -1
    rgb = [255, 0, 0]

    for r_m, g_m, b_m in [
        (0, 0, 1),
        (-1, 0, 0),
        (0, 1, 0),
        (0, 0, -1),
        (1, 0, 0),
    ]:
        for _ in range(255):
            index += 1

            rgb[0] = rgb[0] + (1 * r_m)
            rgb[1] = rgb[1] + (1 * g_m)
            rgb[2] = rgb[2] + (1 * b_m)

            data[index] = tuple(rgb)

    return data


class Palette(object):

    data: dict[int, str]

    def __init__(self, data: dict) -> None:
        self.data = data

    def get(self, value: int):
        return self.data.get(value, (255, 255, 255))

    @classmethod
    def rgb(cls):
        return cls(gen_rgb())

    @classmethod
    def step_rgb(cls, step: int = 255):
        data = gen_rgb()
        new_data = {}

        new_index = 0

        for index in data:
            if index % step == 0:
                new_data[new_index] = data[index]
                new_index += 1

        return cls(new_data)

    @classmethod
    def black_white(cls):
        return cls({0: (0, 0, 0), 1: (255, 255, 255)})

    @classmethod
    def blue_green(cls):
        return cls({0: (36, 43, 179), 1: (2, 171, 10)})

    @classmethod
    def set_color_pair(cls, zero_color: Tuple, one_color: Tuple):
        return cls({0: zero_color, 1: one_color})


class DynamicPalette(Palette):

    last_sec: int
    step: int

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.last_sec = math.floor(time.time())
        self.step = 1
        self.data_len = len(self.data)

    def change(self):
        new_data = {}

        for index, color in self.data.items():
            new_data[(index + self.step) % self.data_len] = color

        self.data = new_data

        # self.step += 1

    def get(self, value: int):
        now = math.floor(time.time())

        if now != self.last_sec:
            self.last_sec = now
            self.change()

        return self.data.get(value, (255, 255, 255))


class InversionPalette(DynamicPalette):

    last_sec: int

    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.last_sec = math.floor(time.time())

    def change(self):
        for index, color in self.data.items():
            self.data[index] = 255 - color[0], 255 - color[1], 255 - color[2]
