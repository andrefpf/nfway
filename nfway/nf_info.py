from dataclasses import dataclass
from decimal import Decimal
from datetime import date, time


@dataclass(frozen=True)
class NFItem:
    name: str
    quantity: int | float
    quantity_unit: str
    unit_value: Decimal
    item_value: Decimal
    code: str


@dataclass(frozen=True)
class NFInfo:
    items: tuple[NFItem]
    total_value: Decimal
    total_taxes: Decimal

    emission_date: date | None
    emission_time: time | None

    emiter_name: str = ""
    emiter_cnpj: str = ""
    emiter_address: str = ""
    emiter_coords: tuple[int, int] | None = None

    number: str = ""
    series: str = ""
    access_key: str = ""

