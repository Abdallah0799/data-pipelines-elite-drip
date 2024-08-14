

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`charges`
  OPTIONS()
  as with
    charges as (
        select * from `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
    )

select * from charges;

