CREATE TABLE customers (
  customer_id VARCHAR PRIMARY KEY,
  customer_name VARCHAR,
  region VARCHAR,
  signup_date DATE
);

CREATE TABLE products (
  product_id VARCHAR PRIMARY KEY,
  product_name VARCHAR,
  category VARCHAR,
  subcategory VARCHAR,
  price NUMERIC
);

CREATE TABLE orders (
  order_id VARCHAR PRIMARY KEY,
  customer_id VARCHAR REFERENCES customers(customer_id),
  order_date DATE,
  channel VARCHAR,
  status VARCHAR,
  shipping_cost NUMERIC,
  tax NUMERIC,
grand_total NUMERIC
);

CREATE TABLE order_items (
  id SERIAL PRIMARY KEY,
  order_id VARCHAR REFERENCES orders(order_id),
  product_id VARCHAR REFERENCES products(product_id),
  quantity INTEGER,
  unit_price NUMERIC,
  line_total NUMERIC
);
Load CSVs (on server where Postgres can access files) using psql or COPY:

sql
Copy code
-- from psql shell (server-side file path)
\copy customers FROM '/path/to/customers.csv' CSV HEADER;
\copy products FROM '/path/to/products.csv' CSV HEADER;
\copy orders FROM '/path/to/orders.csv' CSV HEADER;
\copy order_items FROM '/path/to/order_items.csv' CSV HEADER;
SELECT p.product_id, p.product_name, SUM(oi.line_total) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC
LIMIT 10;

-- Monthly sales (revenue) trend
SELECT DATE_TRUNC('month', o.order_date) AS month, SUM(o.grand_total) AS revenue, COUNT(*) AS orders
FROM orders o
WHERE o.status='Delivered'
GROUP BY 1
ORDER BY 1;
SELECT c.region, COUNT(o.order_id) AS orders, SUM(o.grand_total) AS revenue, AVG(o.grand_total) AS avg_order_value
FROM orders o JOIN customers c ON o.customer_id=c.customer_id
WHERE o.status='Delivered'
GROUP BY c.region
ORDER BY revenue DESC;

-- % of returned orders
SELECT SUM(CASE WHEN status='Returned' THEN 1 ELSE 0 END)::float / COUNT(*) AS return_rate
FROM orders;
