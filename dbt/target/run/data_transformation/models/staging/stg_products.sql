

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_products`
  OPTIONS()
  as with 

source as (
    select * from `mycenter-425712.fictive_company.products`
)

select * from source;

