WITH source AS (
    SELECT * FROM {{ source('bq_warehouse', 'products') }}
)

SELECT * FROM source
