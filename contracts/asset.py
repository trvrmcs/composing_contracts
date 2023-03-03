from enum import Enum


class Asset(Enum):
    BTC = "BTC"
    ETH = "ETH"
    CAD = "CAD"
    USD = "USD"

    def __repr__(self):
        return self.value
