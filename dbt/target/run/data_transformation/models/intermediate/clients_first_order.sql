

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`clients_first_order`
  OPTIONS()
  as with
    orders as (
        select * from `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
    )

SELECT 
    customer_id, 
    MIN(order_date) AS first_order_date
FROM 
    orders
GROUP BY 
    customer_id;

