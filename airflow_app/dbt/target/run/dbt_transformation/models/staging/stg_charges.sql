

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`stg_charges`
  OPTIONS()
  as WITH source AS (
    SELECT * FROM `mycenter-425712`.`fictive_company`.`charges`
)

SELECT * FROM source;

