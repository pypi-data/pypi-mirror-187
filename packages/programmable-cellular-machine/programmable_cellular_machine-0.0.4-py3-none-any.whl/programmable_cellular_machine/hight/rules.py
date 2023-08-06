from programmable_cellular_machine.rules import BaseRule
import numba as nb

import numba as nb
from numba import int16

from programmable_cellular_machine.hight import hight_load
from programmable_cellular_machine.places import BasePlace


class BaseHightRule(BaseRule):
    """Базовый класс для высоко производительных правил с своими ограничениями"""


class ConfigurableRule(BaseHightRule):
    birth_trigger: list[int]
    survival_trigger: list[int]
    radius: int

    def __init__(
        self, iterations: int, birth_trigger: list[int] | str, survival_trigger: list[int] | str, radius: int = 1
    ) -> None:
        super().__init__(iterations)

        self.birth_trigger = birth_trigger
        if isinstance(birth_trigger, str):
            self.birth_trigger = [int(i) for i in birth_trigger]

        self.survival_trigger = survival_trigger
        if isinstance(survival_trigger, str):
            self.survival_trigger = [int(i) for i in survival_trigger]

        self.birth_trigger = nb.typed.List(self.birth_trigger) or nb.typed.List.empty_list(int16)
        self.survival_trigger = nb.typed.List(self.survival_trigger) or nb.typed.List.empty_list(int16)

        self.radius = radius

    def implement(self, pos_x: int, pos_y: int, value: int, place: BasePlace) -> int:
        return hight_load.configurable_rule_implement(
            place.data,
            pos_x,
            pos_y,
            value,
            self.radius,
            self.birth_trigger,
            self.survival_trigger,
        )


class LifeRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '2', '23')


class DayAndNightRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '3678', '34678')


class MazeRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '3', '12345')


class SeedsRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '2', '')


class LifeWithoutDeathRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '3', '012345678')


class HighLifeRule(ConfigurableRule):
    def __init__(self, iterations: int) -> None:
        super().__init__(iterations, '36', '23')
