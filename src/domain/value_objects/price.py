from dataclasses import dataclass
from enum import Enum


class CurrencyOption(Enum):
    euro = "EUR"
    dollar = "USD"


@dataclass(frozen=True)
class Price:
    value: float
    currency: CurrencyOption
