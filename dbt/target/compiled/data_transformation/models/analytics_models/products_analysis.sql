SELECT 
    products.title AS product_name,
    SUM(oi.quantity) AS total_sales,
    SUM(oi.quantity * products.unit_amount) AS total_revenue,
    SUM(oi.quantity * products.unit_amount) / SUM(oi.quantity) AS avg_sale_price,
    COUNT(DISTINCT o.customer_id) AS total_unique_customers,
    MIN(o.order_date) AS first_purchase_date

FROM
		`mycenter-425712.fictive_company.order_items` oi

LEFT JOIN 
		`mycenter-425712.fictive_company.orders` o ON oi.order_id = o.id

LEFT JOIN 
		`mycenter-425712.fictive_company.products` products ON oi.product_id = products.id

GROUP BY 
    products.title