from decimal import Decimal

def price_volume(x: tuple[float, float]):
    return Decimal(x[0]), Decimal(x[1])

def get_price_from_tuple(x: tuple[float, float]) -> Decimal:
    return Decimal(x[0])

def get_volume_from_tuple(x: tuple[float, float]) -> Decimal:
    return Decimal(x[1])

def get_bids(x: dict) -> list[tuple[float, float]]:
    return x['bids']

def get_asks(x: dict) -> list[tuple[float, float]]:
    return x['asks']