INSERT INTO products (id, name, description, sku) VALUES
(1, 'Laptop', 'Gaming Laptop', 'LAP123');

INSERT INTO attributes (id, product_id, name) VALUES
(1, 1, 'Color');

INSERT INTO attribute_values (id, attribute_id, value) VALUES
(1, 1, 'Black');

INSERT INTO rental_periods (id, duration_months) VALUES
(1, 3);

INSERT INTO regions (id, name) VALUES
(1, 'Singapore');

INSERT INTO product_pricings (id, product_id, rental_period_id, region_id, price) VALUES
(1, 1, 1, 1, 100.0);