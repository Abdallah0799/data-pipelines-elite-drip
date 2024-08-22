WITH source AS (
    SELECT * FROM {{ source('bq_warehouse', 'order_items') }}
)

SELECT * FROM source
