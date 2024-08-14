with
    orders as (
        select * from {{ref('stg_orders')}}
    )

SELECT 
    customer_id, 
    MIN(order_date) AS first_order_date
FROM 
    orders
GROUP BY 
    customer_id