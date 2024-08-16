from google.cloud import bigquery


class BigQuerySchemas:

    orders = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("order_date", "DATE"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("country", "STRING"),
        bigquery.SchemaField("customer_id", "INT64"),
        bigquery.SchemaField("amount", "FLOAT64"),
        bigquery.SchemaField("total_items", "INT64")
    ]

    products = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("unit_amount", "FLOAT64"),
        bigquery.SchemaField("gender", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("created_at", "DATE")
    ]

    order_items = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("order_id", "INT64"),
        bigquery.SchemaField("product_id", "INT64"),
        bigquery.SchemaField("quantity", "INT64")
    ]

    charges = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("order_id", "INT64"),
        bigquery.SchemaField("amount", "FLOAT64")
    ]
