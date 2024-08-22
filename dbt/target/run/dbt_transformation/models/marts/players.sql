

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`players`
  OPTIONS()
  as WITH  __dbt__cte__clients_first_order as (
WITH orders AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
)

SELECT 
    customer_id, 
    MIN(order_date) AS first_order_date
FROM 
    orders
GROUP BY 
    customer_id
), players AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_players`
),

clients_first_order AS (
    SELECT * 
    FROM __dbt__cte__clients_first_order
)

SELECT 
    p.*, 
    cfo.first_order_date
FROM 
    players p
LEFT JOIN 
    clients_first_order cfo 
    ON p.id = cfo.customer_id;

