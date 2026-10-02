"""Domain models shared by page objects and tests.

Page objects return these instead of raw strings, so tests compare
business objects (`Product`, `OrderSummary`) rather than scraped text.
"""
import re
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from typing import Iterable

TAX_RATE = Decimal("0.08")
CENT = Decimal("0.01")


def money(text: str) -> Decimal:
    """'$29.99' or 'Item total: $29.99' -> Decimal('29.99')."""
    match = re.search(r"\$(\d+(?:\.\d+)?)", text)
    if not match:
        raise ValueError(f"No amount found in {text!r}")
    return Decimal(match.group(1))


@dataclass(frozen=True)
class User:
    username: str
    password: str


@dataclass(frozen=True)
class Product:
    name: str
    price: Decimal
    # Not part of equality: catalog test data doesn't carry descriptions.
    description: str = field(default="", compare=False)


@dataclass(frozen=True)
class Customer:
    first_name: str
    last_name: str
    postal_code: str


@dataclass(frozen=True)
class OrderSummary:
    item_total: Decimal
    tax: Decimal
    total: Decimal

    @classmethod
    def expected_for(cls, products: Iterable[Product]) -> "OrderSummary":
        """What the overview page should show for these products (8% tax, rounded half-up)."""
        item_total = sum((p.price for p in products), Decimal("0"))
        tax = (item_total * TAX_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
        return cls(item_total, tax, item_total + tax)
