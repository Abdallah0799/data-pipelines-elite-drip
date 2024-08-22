

  create or replace view `mycenter-425712`.`fictive_company_transformation`.`order_items`
  OPTIONS()
  as WITH orders AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
),

order_items AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_order_items`
),

products AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_products`
),

players AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_players`
)

SELECT 
    orders.*, 
    order_items.* EXCEPT (id, created_at, updated_at),
    products.* EXCEPT (id, created_at, updated_at),
    players.* EXCEPT (id, created_at, updated_at)
FROM 
    order_items
JOIN 
    orders ON orders.id = order_items.order_id
JOIN 
    products ON order_items.product_id = products.id
JOIN 
    players ON players.id = orders.customer_id;

