

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`charges`
  OPTIONS()
  as WITH charges AS (
    SELECT * FROM `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
)

SELECT * FROM charges;

