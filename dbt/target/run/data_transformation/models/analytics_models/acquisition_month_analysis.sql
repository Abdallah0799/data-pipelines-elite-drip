

  create or replace view `mycenter-425712`.`fictive_company`.`acquisition_month_analysis`
  OPTIONS()
  as WITH ClientFirstOrder AS (
    SELECT 
        customer_id, 
        MIN(order_date) AS first_order_date
    FROM 
        `mycenter-425712.fictive_company.orders`
    GROUP BY 
        customer_id
),

CohortMonthlyLTV AS (
    SELECT 
        FORMAT_DATE('%Y-%m', cfo.first_order_date) AS cohort_month,
        DATE_DIFF(o.order_date, cfo.first_order_date, MONTH) AS order_month,
        SUM(o.amount) AS monthly_ltv
    FROM 
        `mycenter-425712.fictive_company.orders` o
    JOIN 
        ClientFirstOrder cfo ON cfo.customer_id = o.customer_id
    GROUP BY 
        cohort_month, 
        order_month
    ORDER BY 
        cohort_month, 
        order_month
)

SELECT 
    *,
    SUM(monthly_ltv) OVER (PARTITION BY cohort_month ORDER BY order_month) AS ltv
FROM 
    CohortMonthlyLTV
ORDER BY 
    cohort_month, 
    order_month;

