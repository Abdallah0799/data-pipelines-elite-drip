WITH orders AS (
    SELECT * 
    FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * 
    FROM {{ ref('stg_order_items') }}
),

products AS (
    SELECT * 
    FROM {{ ref('stg_products') }}
),

players AS (
    SELECT * 
    FROM {{ ref('stg_players') }}
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
    players ON players.id = orders.customer_id
