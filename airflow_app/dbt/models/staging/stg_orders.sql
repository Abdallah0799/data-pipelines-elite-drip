WITH source AS (
    SELECT * FROM {{ source('bq_warehouse', 'orders') }}
)

SELECT * FROM source
