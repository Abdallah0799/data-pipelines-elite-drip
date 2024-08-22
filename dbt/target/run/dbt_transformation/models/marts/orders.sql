

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`orders`
  OPTIONS()
  as WITH  __dbt__cte__charge_by_order as (
WITH charges AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
)

SELECT 
    order_id, 
    SUM(amount) AS total_charges
FROM 
    charges
GROUP BY 
    order_id
), orders AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
),

charges_by_order AS (
    SELECT * 
    FROM __dbt__cte__charge_by_order
)

SELECT 
    orders.*, 
    COALESCE(cbo.total_charges, 0) AS total_charges
FROM 
    orders
LEFT JOIN 
    charges_by_order cbo 
    ON orders.id = cbo.order_id;

