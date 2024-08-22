WITH charges AS (
    SELECT * 
    FROM {{ ref('stg_charges') }}
)

SELECT 
    order_id, 
    SUM(amount) AS total_charges
FROM 
    charges
GROUP BY 
    order_id
