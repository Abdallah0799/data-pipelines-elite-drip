WITH source AS (
    SELECT * FROM {{ source('bq_warehouse', 'players') }}
)

SELECT * FROM source
