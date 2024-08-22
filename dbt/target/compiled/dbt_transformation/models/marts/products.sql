WITH order_items AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`order_items`
),

products AS (
    SELECT *
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_products`
)

SELECT
    products.title AS product_name,
    SUM(o.quantity) AS total_sales,
    SUM(o.quantity * products.unit_amount) AS total_revenue,
    SUM(o.quantity * products.unit_amount) / NULLIF(SUM(o.quantity), 0) AS avg_sale_price,
    COUNT(DISTINCT o.customer_id) AS total_unique_customers,
    MIN(o.order_date) AS first_purchase_date
FROM
    order_items o
LEFT JOIN
    products 
    ON o.product_id = products.id
GROUP BY
    products.title