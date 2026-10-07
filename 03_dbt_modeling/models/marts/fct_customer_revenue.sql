-- Marts Model: Business summary table
SELECT 
    customer_id,
    COUNT(order_id) as total_orders,
    ROUND(SUM(amount), 2) as lifetime_revenue
FROM {{ ref('stg_orders') }}
GROUP BY customer_id
ORDER BY lifetime_revenue DESC
