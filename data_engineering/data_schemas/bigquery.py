from google.cloud import bigquery

orders = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("created_at", "TIMESTAMP"),
        bigquery.SchemaField("updated_at", "TIMESTAMP"),
        bigquery.SchemaField("order_date", "TIMESTAMP"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("customer_id", "INT64"),
        bigquery.SchemaField("amount", "FLOAT64"),
        bigquery.SchemaField("total_items", "INT64")
    ]

products = [
    bigquery.SchemaField("id", "INT64"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("updated_at", "TIMESTAMP"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("unit_amount", "FLOAT64"),
    bigquery.SchemaField("gender", "STRING"),
    bigquery.SchemaField("category", "STRING")
]

order_items = [
    bigquery.SchemaField("id", "INT64"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("updated_at", "TIMESTAMP"),
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("product_id", "INT64"),
    bigquery.SchemaField("quantity", "INT64")
]

charges = [
    bigquery.SchemaField("id", "INT64"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("updated_at", "TIMESTAMP"),
    bigquery.SchemaField("order_id", "INT64"),
    bigquery.SchemaField("amount", "FLOAT64")
]

players = [
    bigquery.SchemaField("id", "INT64"),
    bigquery.SchemaField("created_at", "TIMESTAMP"),
    bigquery.SchemaField("updated_at", "TIMESTAMP"),
    bigquery.SchemaField("first_name", "STRING"),
    bigquery.SchemaField("last_name", "STRING"),
    bigquery.SchemaField("email", "STRING"),
    bigquery.SchemaField("delivery_city", "STRING"),
    bigquery.SchemaField("team_name", "STRING"),
]
