-- 1. Total orders per customer
SELECT
    customer_id,
    customer_name,
    COUNT(*) AS total_orders
FROM
    orders
GROUP BY
    customer_id,
    customer_name
ORDER BY
    total_orders DESC;

-- 2. Total amount spent per customer
SELECT
    customer_id,
    customer_name,
    SUM(amount) AS total_spent
FROM
    orders
GROUP BY
    customer_id,
    customer_name
ORDER BY
    total_spent DESC;

-- 3. Top 2 customers by total spend
SELECT
    customer_id,
    customer_name,
    SUM(amount) AS total_spent
FROM
    orders
GROUP BY
    customer_id,
    customer_name
ORDER BY
    total_spent DESC
LIMIT 2;