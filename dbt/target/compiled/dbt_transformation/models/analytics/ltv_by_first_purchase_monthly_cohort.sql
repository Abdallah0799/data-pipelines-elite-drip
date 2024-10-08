WITH  __dbt__cte__clients_first_order as (
WITH orders AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
)

SELECT 
    customer_id, 
    MIN(order_date) AS first_order_date
FROM 
    orders
GROUP BY 
    customer_id
), orders AS (
    SELECT * 
    FROM `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
),

clients_first_order AS (
    SELECT * 
    FROM __dbt__cte__clients_first_order
),

CohortMonthlyLTV AS (
    SELECT 
        FORMAT_DATE('%Y-%m', cfo.first_order_date) AS cohort_month,
        DATE_DIFF(DATETIME(o.order_date), DATETIME(cfo.first_order_date), MONTH) AS order_month,
        SUM(o.amount) AS monthly_ltv
    FROM 
        orders o
    JOIN 
        clients_first_order cfo 
        ON cfo.customer_id = o.customer_id
    GROUP BY 
        cohort_month, 
        order_month
    ORDER BY 
        cohort_month, 
        order_month
)

SELECT 
    *,
    SUM(monthly_ltv) OVER (
        PARTITION BY cohort_month 
        ORDER BY order_month
    ) AS ltv
FROM 
    CohortMonthlyLTV
ORDER BY 
    cohort_month, 
    order_month