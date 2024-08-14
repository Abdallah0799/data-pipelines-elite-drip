

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
  OPTIONS()
  as with 

source as (
    select * from `mycenter-425712.fictive_company.charges`
)

select * from source;

