

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_order_items`
  OPTIONS()
  as WITH source AS (
    SELECT * FROM `mycenter-425712`.`fictive_company`.`order_items`
)

SELECT * FROM source;

