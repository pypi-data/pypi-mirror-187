from dataclasses import dataclass
from decimal import Decimal
import decimal

from logging import getLogger

logger = getLogger(__name__)

def compute_grid_orders(
    bid_price: Decimal,
    ask_price: Decimal,
    amount_per_order: Decimal,
    gap: Decimal,
    order_count: int,
    quantity_decimal_places: int,
) -> list[tuple[tuple[Decimal, Decimal]]]:
    levels = []
    with decimal.localcontext() as context:
        context.rounding = decimal.ROUND_DOWN
        for i in range(order_count):
            multiplier = Decimal(i+1/2)
            price = bid_price - multiplier * gap
            quantity = round(amount_per_order / price, quantity_decimal_places)
            levels.append((
                (price, quantity), (ask_price + multiplier * gap, quantity)
            ))

    return levels

__all__ = [
    "compute_grid_orders"
]