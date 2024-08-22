WITH orders AS (
    SELECT * 
    FROM {{ ref('stg_orders') }}
),

charges_by_order AS (
    SELECT * 
    FROM {{ ref('charge_by_order') }}
)

SELECT 
    orders.*, 
    COALESCE(cbo.total_charges, 0) AS total_charges
FROM 
    orders
LEFT JOIN 
    charges_by_order cbo 
    ON orders.id = cbo.order_id
