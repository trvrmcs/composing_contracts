from typing import TypeVar, Generic
from adt import adt, Case

T = TypeVar("T")


@adt
class Observable(Generic[T]):
    CONST: Case[T]
    # Date: Case

    def __repr__(self):
        return f"{self._key.name}({self._value})"
