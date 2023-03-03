from adt import adt, Case
from decimal import Decimal
import datetime as dt

from .asset import Asset
from .observable import Observable


@adt
class Contract:
    ZERO: Case
    ONE: Case[Asset]
    GIVE: Case["Contract"]
    AND: Case["Contract", "Contract"]
    OR: Case["Contract", "Contract"]
    CONDITION: Case[Observable[bool], "Contract", "Contract"]
    SCALE: Case[Observable[Decimal], "Contract"]
    WHEN: Case[dt.date, "Contract"]


def _rv(v):
    if isinstance(v, dt.date):
        return v.isoformat()
    else:
        return repr(v)


def _repr(self):
    name = self._key.name
    value = self._value
    if value is None:
        return f"{name}()"
    if isinstance(value, tuple):
        return f"{name}({','.join(_rv(v) for v in value)})"

    return f"{name}({repr(value)})"


Contract.__repr__ = _repr
