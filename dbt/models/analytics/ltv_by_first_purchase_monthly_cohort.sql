WITH orders AS (
    SELECT * 
    FROM {{ ref('stg_orders') }}
),

clients_first_order AS (
    SELECT * 
    FROM {{ ref('clients_first_order') }}
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
