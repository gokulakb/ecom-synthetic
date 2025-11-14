-- queries.sql

-- 1) Top 10 customers by total spent
SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,
       c.email,
       COUNT(o.order_id) AS num_orders,
       SUM(o.order_total) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 2) Detailed order with items and shipment info for a given order_id (replace ? with desired id)
SELECT o.order_id, o.order_date, o.status, o.order_total,
       c.first_name || ' ' || c.last_name AS customer_name,
       s.shipped_at, s.carrier, s.tracking_number,
       oi.order_item_id, p.name AS product_name, oi.quantity, oi.unit_price, oi.line_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN shipments s ON o.order_id = s.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_id = 1
ORDER BY oi.order_item_id;

-- 3) Monthly sales by category
SELECT strftime('%Y-%m', o.order_date) AS month, p.category, SUM(oi.line_total) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY month, p.category
ORDER BY month DESC, revenue DESC;
