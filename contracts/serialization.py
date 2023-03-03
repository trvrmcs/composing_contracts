from typing import List, Union
from decimal import Decimal
import json
from .observable import Observable
from .contract import Contract
from .asset import Asset


def observable_to_list(observable: Observable) -> List:
    return observable.match(
        const=lambda x: ["CONST", x],
        # date = lambda d: ['DATE',str(d)]
    )


def contract_to_list(contract: Contract) -> List:
    return contract.match(
        ZERO=lambda: ["ZERO"],
        ONE=lambda asset: ["ONE", asset.name],
        GIVE=lambda c: ["GIVE", to_list(c)],
        AND=lambda left, right: ["AND", to_list(left), to_list(right)],
        OR=lambda left, right: ["OR", to_list(left), to_list(right)],
        CONDITION=lambda obs, left, right: [
            "CONDITION",
            to_list(obs),
            to_list(left),
            to_list(right),
        ],
        SCALE=lambda obs, c: ["SCALE", to_list(obs), to_list(c)],
        WHEN=lambda d, c: ["WHEN", str(d), to_list(c)],
    )


def to_list(thing: Union[Contract, Observable]) -> List:
    try:
        return {Contract: contract_to_list, Observable: observable_to_list}[
            type(thing)
        ](thing)
    except KeyError:
        raise Exception(f"KeyError with {thing}")


def _unpack(thing: Union[List, str, float, int]):
    if isinstance(thing, list):
        return from_list(thing)

    if isinstance(thing, str):
        if hasattr(Asset, thing):
            return getattr(Asset, thing)

    if isinstance(thing, (float, int)):
        return Decimal(str(thing))

    raise Exception(f"Unhandled case: {thing}")


def from_list(l: List) -> Contract:
    if isinstance(l, str):
        if hasattr(Asset, l):
            return getattr(Asset, l)

    if not isinstance(l, list):
        return l

    head, *tail = l
    assert head.upper() == head

    args = [_unpack(el) for el in tail]

    if hasattr(Contract, head):
        return getattr(Contract, head)(*args)
    elif hasattr(Observable, head):
        return getattr(Observable, head)(*args)
    else:
        raise Exception(f"Unknown constructor: {head}")


def pprint(contract):
    print(dumps(contract))


def loads(s):
    return from_list(json.loads(s))


def dumps(contract, indent=None):
    return json.dumps(to_list(contract), indent=indent)
