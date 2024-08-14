

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_order_items`
  OPTIONS()
  as with 

source as (
    select * from `mycenter-425712.fictive_company.order_items`
)

select * from source;

