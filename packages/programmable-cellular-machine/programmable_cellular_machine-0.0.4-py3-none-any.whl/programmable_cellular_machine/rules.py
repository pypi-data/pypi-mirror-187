import abc
import random
from time import sleep
from typing import Callable

import numba as nb
from numba import int16, int32

from programmable_cellular_machine.hight import hight_load
from programmable_cellular_machine.places import BasePlace


class BaseRule(abc.ABC):
    iterations: int

    def __init__(self, iterations: int) -> None:
        self.iterations = iterations

    @abc.abstractmethod
    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace):
        pass


class TimeRule(BaseRule):
    time_sleep: int

    def __init__(self, iterations: int, time_sleep: int = 0.0001) -> None:
        super().__init__(iterations)
        self.time_sleep = time_sleep

    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace):
        sleep(self.time_sleep)
        return value


class LambdaRule(BaseRule):
    def __init__(self, iterations: int, func: Callable) -> None:
        super().__init__(iterations)

        self.func = func

    def implement(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def make_func__random_place_with(cls, value: int, proc: float):
        def inner(*args, **kwargs):
            return value if round(random.random(), 2) == proc else 0

        return inner


class IncrementRule(BaseRule):
    def __init__(self, iterations: int, increment: int) -> None:
        super().__init__(iterations)

        self.increment = increment

    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace):
        return value + self.increment


class RandomRule(BaseRule):

    min_value: int
    max_value: int

    def __init__(self, iterations: int, min_value: int = 0, max_value: int = 1) -> None:
        super().__init__(iterations)

        self.min_value = min_value
        self.max_value = max_value

    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace):
        return random.randint(self.min_value, self.max_value)


class BelousovZhabotinskyRule(BaseRule):
    number_types: int

    def __init__(self, iterations: int, number_types: int) -> None:
        super().__init__(iterations)
        self.number_types = number_types

    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace):
        target_value = value + 1
        if target_value == self.number_types:
            target_value = 0

        lives = 0

        for _, _, sub_value in place.radius(pos_x, pos_y, 1):
            if sub_value == target_value:
                lives += 1

        if lives >= 3:
            return target_value

        return value
