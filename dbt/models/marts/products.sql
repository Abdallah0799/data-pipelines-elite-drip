{{
    config(
        materialized='view'
    )
}}

with 

orders as (
    select * from {{ref('orders')}}
),

products as (
    select * from {{ref('stg_products')}}
)

SELECT 
    products.title AS product_name,
    SUM(o.quantity) AS total_sales,
    SUM(o.quantity * products.unit_amount) AS total_revenue,
    SUM(o.quantity * products.unit_amount) / SUM(o.quantity) AS avg_sale_price,
    COUNT(DISTINCT o.customer_id) AS total_unique_customers,
    MIN(o.order_date) AS first_purchase_date,

FROM orders o

LEFT JOIN 
	products ON o.product_id = products.id

GROUP BY 
    products.title