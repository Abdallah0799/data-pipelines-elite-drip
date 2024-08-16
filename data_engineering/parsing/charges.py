from dataclasses import dataclass

from . import BaseSchema


@dataclass
class Charge(BaseSchema):
    # Class fields
    from_db = 'mongodb'
    source_name = 'charges'

    # Instance fields
    id: int
    order_id: str
    amount: float


def parse_raw_charges(raw_charge: dict) -> Charge:

    return Charge(
        id=raw_charge['id'] if 'id' in raw_charge else None,
        order_id=raw_charge['order_id'] if 'order_id' in raw_charge else None,
        amount=raw_charge['amount'] if 'amount' in raw_charge else None
    )
