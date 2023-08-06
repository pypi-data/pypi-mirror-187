import math
import time
import random
from programmable_cellular_machine.places import BasePlace
from programmable_cellular_machine.rules import BaseRule
from programmable_cellular_machine.utils import time_measurement
from programmable_cellular_machine.visual import VisualProvider


class CellularMachine(object):
    """Клеточный автомат"""

    # Набор правил
    rules: list[BaseRule]

    # Стартовое полотно. Шаблон
    start_place: BasePlace
    # Конечное полотно. Результат
    last_place: BasePlace | None

    def __init__(
        self,
        start_place: BasePlace,
        rules: list[BaseRule],
        seed: int | float | str | bytes | bytearray | None = None
    ) -> None:

        random.seed(seed)
        self.rules = rules

        self.start_place = start_place
        self.last_place = None

        self.seconds = []

    def make_new_place(self) -> BasePlace:
        return self.start_place.make_layout()

    def inner_implement_rule(self, place: BasePlace, rule: BaseRule):
        new_place = self.make_new_place()

        for pos_x, pos_y, value in place.cells:
            new_value = rule.implement(pos_x, pos_y, value, place)
            new_place.set(pos_x, pos_y, new_value)

        return new_place

    def implement_rule(self, place: BasePlace, rule: BaseRule):
        return self.inner_implement_rule(place, rule)

    def iter_in_sec(self):
        now = math.floor(time.time())

        if self.seconds and self.seconds[0] != now:
            print(f'{len(self.seconds)} вызовов в секунду')
            self.seconds = []

        self.seconds.append(now)

    def generate(self):
        number_iterations = 0
        place = self.start_place

        for rule in self.rules:
            for _ in range(rule.iterations):
                number_iterations += 1

                print(f'Итерация №{number_iterations} | Правило: {rule}')

                place = self.implement_rule(place, rule)

                self.iter_in_sec()

                yield place

    def start(self):
        pass

    def stop(self):
        pass

    def inner_run(self, visual_provider: VisualProvider):
        place = None

        for place in self.generate():
            visual_provider.render(place)

        self.last_place = place

    @time_measurement
    def run(self, visual_provider: VisualProvider):
        self.start()
        visual_provider.start(self.start_place)

        try:
            self.inner_run(visual_provider)

        except BaseException as ex:
            visual_provider.stop(None)
            self.stop()
            raise ex

        else:
            visual_provider.stop(self.last_place)
            self.stop()
