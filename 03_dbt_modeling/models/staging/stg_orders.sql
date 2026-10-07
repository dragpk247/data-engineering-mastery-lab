-- Staging Model: Clean and type cast raw source orders
WITH raw_orders AS (
    SELECT 
        'ord_101' as order_id, 'cust_1' as customer_id, 150.00 as amount, 'COMPLETED' as status UNION ALL
    SELECT 
        'ord_102', 'cust_2', 89.50, 'COMPLETED' UNION ALL
    SELECT 
        'ord_103', 'cust_1', 210.00, 'COMPLETED' UNION ALL
    SELECT 
        'ord_104', 'cust_3', 35.00, 'REFUNDED' UNION ALL
    SELECT 
        'ord_105', 'cust_2', 120.00, 'COMPLETED'
)

SELECT 
    order_id,
    customer_id,
    amount,
    status
FROM raw_orders
WHERE status = 'COMPLETED'
