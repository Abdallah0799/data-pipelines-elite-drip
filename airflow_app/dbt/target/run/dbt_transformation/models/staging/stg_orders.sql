

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
  OPTIONS()
  as WITH source AS (
    SELECT * FROM `mycenter-425712`.`fictive_company`.`orders`
)

SELECT * FROM source;

