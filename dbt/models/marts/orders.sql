{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

with

orders as (
    select * from {{ref('stg_orders')}}
),

order_items as (
    select * from {{ref('stg_order_items')}}
),

products as (
    select * from {{ref('stg_products')}}
),

charges_by_order as (
    select * from {{ref('charge_by_order')}}
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

{% if is_incremental() %}

where
  orders.order_date > (select max(orders.order_date) from {{ this }})

{% endif %}
