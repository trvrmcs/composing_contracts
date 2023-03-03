from typing import Callable
from decimal import Decimal
from datetime import date, timedelta

from math import exp, sqrt
import random


# ooh, static duck typing!
Process = Callable[date, Decimal]

STEPS = 365
START = date(2023, 3, 3)
END = START + timedelta(days=STEPS)


DAYS = [START + timedelta(days=i) for i in range(STEPS)]


class ConstProcess:
    def __init__(self, value: Decimal) -> None:
        self.value = value

    def __call__(self, d: date) -> Decimal:
        assert d >= START
        assert d < END
        return self.value


class BinomialPriceProcess:
    def __init__(self, initial: Decimal, sigma: float) -> None:
        deltaT = 1 / STEPS
        up = exp(sigma * sqrt(deltaT))
        down = exp(-sigma * sqrt(deltaT))

        p = (1 - down) / (up - down)

        moves = random.choices([up, down], weights=[p, 1 - p], k=STEPS)

        def inner():
            nonlocal initial
            for move in moves:
                yield initial
                initial = initial * Decimal(move)

        self.values = [round(value, 2) for value in inner()]

    def __call__(self, d: date) -> Decimal:
        assert d >= START
        assert d < END
        index = (d - START).days
        return self.values[index]
