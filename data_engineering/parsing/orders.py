from dataclasses import dataclass
import datetime

from . import BaseSchema


@dataclass
class Order(BaseSchema):
    # Class fields
    from_db = "mongodb"
    source_name = "orders"

    # Instance fields
    id: int
    order_date: datetime
    status: str
    country: str
    customer_id: int
    amount: float
    total_items: int


def parse_raw_orders(raw_order: dict) -> Order:

    return Order(
        id=raw_order["id"] if "id" in raw_order else None,
        order_date=(raw_order["order_date"] if "order_date" in raw_order else None),
        status=raw_order["status"] if "status" in raw_order else None,
        country=raw_order["country"] if "country" in raw_order else None,
        customer_id=(raw_order["customer_id"] if "customer_id" in raw_order else None),
        amount=raw_order["amount"] if "amount" in raw_order else None,
        total_items=(raw_order["total_items"] if "total_items" in raw_order else None),
    )
