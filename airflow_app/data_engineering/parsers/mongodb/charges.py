from dataclasses import dataclass
import datetime


@dataclass
class Charge:
    id: int
    created_at: datetime
    updated_at: datetime
    order_id: str
    amount: float


def parse_charges(raw_charge: dict) -> Charge:

    return Charge(
        id=raw_charge['id'] if 'id' in raw_charge else None,
        created_at=raw_charge['created_at'] if 'created_at' in raw_charge else None,
        updated_at=raw_charge['updated_at'] if 'updated_at' in raw_charge else None,
        order_id=raw_charge['order_id'] if 'order_id' in raw_charge else None,
        amount=raw_charge['amount'] if 'amount' in raw_charge else None
    )
