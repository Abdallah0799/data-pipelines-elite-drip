WITH TotalCharges AS (
    SELECT 
        order_id, 
        SUM(amount) AS total_charges
    FROM 
        `mycenter-425712.fictive_company.charges`
    GROUP BY 
        order_id
)

SELECT 
    o.amount AS order_amount,
    tc.total_charges AS charge_amount,
    o.amount - tc.total_charges AS difference,
    CONCAT(
        CAST(ROUND(
            (o.amount - tc.total_charges) / CAST(o.amount AS DECIMAL), 
            2
        ) * -100 AS STRING), '%'
    ) AS percentage_difference,
    o.status
FROM 
    `mycenter-425712.fictive_company.orders` o
LEFT JOIN 
    TotalCharges tc ON o.id = tc.order_id