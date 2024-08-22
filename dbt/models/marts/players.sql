WITH players AS (
    SELECT * 
    FROM {{ ref('stg_players') }}
),

clients_first_order AS (
    SELECT * 
    FROM {{ ref('clients_first_order') }}
)

SELECT 
    p.*, 
    cfo.first_order_date
FROM 
    players p
LEFT JOIN 
    clients_first_order cfo 
    ON p.id = cfo.customer_id
