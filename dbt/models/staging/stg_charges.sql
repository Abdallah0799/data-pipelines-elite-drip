WITH source AS (
    SELECT * FROM {{ source('bq_warehouse', 'charges') }}
)

SELECT * FROM source
