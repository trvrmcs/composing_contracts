from typing import Callable, Dict
from decimal import Decimal
from datetime import date

Process = Callable[date, Decimal]
from contracts import Contract, Asset, Observable


from .processes import ConstProcess, Process


class Evaluate:
    def __init__(self, processes: Dict[Asset, Process]) -> None:
        self.processes = processes

    def __call__(self, contract: Contract) -> Process:
        return contract.match(
            ZERO=lambda: ConstProcess(Decimal("0")),
            ONE=lambda asset: self.processes[asset],
            GIVE=lambda c: lambda d: -1 * self(c)(d),
            AND=lambda left, right: lambda d: self(left)(d) + self(right)(d),
            OR=lambda left, right: lambda d: max(self(left)(d), self(right)(d)),
            SCALE=lambda obs, c: lambda d: eval_obs(obs)(d) * self(c)(d),
            CONDITION=lambda obs, left, right: lambda d: Decimal("NaN"),  # TODO
            WHEN=lambda _, c: lambda d: self(c)(d),
        )

    # TODO: apply risk-free rate to discount future cashflows in WHEN


def eval_obs(observable: Observable) -> Process:
    return observable.match(const=lambda x: lambda d: x)
