

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`charge_by_order`
  OPTIONS()
  as with
    charges as (
        select * from `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
    )

SELECT 
        order_id, 
        SUM(amount) AS total_charges
FROM 
    charges
GROUP BY 
    order_id;

