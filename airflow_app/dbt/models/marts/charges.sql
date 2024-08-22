WITH charges AS (
    SELECT * FROM {{ref('stg_charges')}}
)

SELECT * FROM charges
