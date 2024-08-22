

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_products`
  OPTIONS()
  as WITH source AS (
    SELECT * FROM `mycenter-425712`.`fictive_company`.`products`
)

SELECT * FROM source;

