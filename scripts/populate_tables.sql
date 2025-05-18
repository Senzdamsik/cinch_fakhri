-- Insert into products
INSERT INTO products (name, description, sku) VALUES
('Laptop', 'High-performance gaming laptop', 'LAP123'),
('Smartphone', 'Latest model smartphone', 'SPH456'),
('Tablet', 'Portable tablet with stylus', 'TAB789');

-- Insert into attributes
INSERT INTO attributes (product_id, name) VALUES
(1, 'Color'),
(1, 'Storage'),
(2, 'Color'),
(2, 'Storage'),
(3, 'Color');

-- Insert into attribute_values
INSERT INTO attribute_values (attribute_id, value) VALUES
(1, 'Black'),
(1, 'Silver'),
(2, '256GB'),
(2, '512GB'),
(3, 'Blue'),
(3, 'Red'),
(4, '128GB'),
(4, '256GB'),
(5, 'White');

-- Insert into rental_periods
INSERT INTO rental_periods (duration_months) VALUES
(3),
(6),
(12);

-- Insert into regions
INSERT INTO regions (name) VALUES
('Singapore'),
('Malaysia');

-- Insert into product_pricings
INSERT INTO product_pricings (product_id, rental_period_id, region_id, price) VALUES
(1, 1, 1, 100.00), -- Laptop, 3 months, Singapore
(1, 1, 2, 90.00),  -- Laptop, 3 months, Malaysia
(1, 2, 1, 180.00), -- Laptop, 6 months, Singapore
(1, 2, 2, 170.00), -- Laptop, 6 months, Malaysia
(1, 3, 1, 350.00), -- Laptop, 12 months, Singapore
(1, 3, 2, 340.00), -- Laptop, 12 months, Malaysia
(2, 1, 1, 80.00),  -- Smartphone, 3 months, Singapore
(2, 1, 2, 75.00),  -- Smartphone, 3 months, Malaysia
(2, 2, 1, 150.00), -- Smartphone, 6 months, Singapore
(2, 2, 2, 140.00), -- Smartphone, 6 months, Malaysia
(3, 1, 1, 60.00),  -- Tablet, 3 months, Singapore
(3, 1, 2, 55.00);  -- Tablet, 3 months, Malaysia