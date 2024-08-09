from dataclasses import dataclass
from google.cloud import bigquery
import datetime

from . import BaseSchema


@dataclass
class Product(BaseSchema):
    # Class fields
    from_db = 'mongodb'
    source_name = 'products'

    # Instance fields
    id: int
    title: str
    unit_amount: float
    gender: str
    category: str
    created_at: datetime


def parse_raw_products(raw_product: dict) -> Product:

    return Product(
        id=raw_product['id'] if 'id' not in raw_product else None,
        title=raw_product['title'] if 'title' not in raw_product else None,
        unit_amount=raw_product['unit_amount'] if 'unit_amount' not in raw_product else None,
        gender=raw_product['gender'] if 'gender' not in raw_product else None,
        category=raw_product['category'] if 'category' not in raw_product else None,
        created_at=raw_product['created_at'] if 'created_at' not in raw_product else None
    )


products_schema = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("unit_amount", "FLOAT64"),
        bigquery.SchemaField("gender", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("created_at", "DATE")
    ]
