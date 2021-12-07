-- 1
SELECT user_name AS "Клиент", ROUND(SUM(price), 2) AS "Общая сумма покупок" FROM orders
JOIN clients ON orders.id_users=clients.id_users
JOIN products ON orders.id_product=products.id_product
GROUP BY user_name;

-- 2

SELECT user_name AS "Клиент" FROM orders
JOIN clients ON orders.id_users=clients.id_users
JOIN products ON orders.id_product=products.id_product
WHERE product_name="Телефон";

-- 3
SELECT products.product_name AS "Клиент", COUNT(orders.id_product) AS "Общая сумма покупок" FROM orders
JOIN products ON orders.id_product=products.id_product
GROUP BY orders.id_product;
