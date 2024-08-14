
  
    

    create or replace table `mycenter-425712`.`fictive_company_transformation`.`orders`
      
    
    

    OPTIONS()
    as (
      

with

orders as (
    select * from `mycenter-425712`.`fictive_company_transformation`.`stg_orders`
),

order_items as (
    select * from `mycenter-425712`.`fictive_company_transformation`.`stg_order_items`
),

products as (
    select * from `mycenter-425712`.`fictive_company_transformation`.`stg_products`
),

charges_by_order as (
    select * from `mycenter-425712`.`fictive_company_transformation`.`charge_by_order`
)

select 
    orders.*, 
    order_items.* except(id),
    products.* except(id),
    IFNULL(cbo.total_charges, 0) AS total_charges

from order_items

join orders

on orders.id = order_items.order_id

join products

on order_items.product_id = products.id

LEFT JOIN
    charges_by_order cbo ON orders.id = cbo.order_id


    );
  