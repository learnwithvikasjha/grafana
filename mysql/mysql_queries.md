# Create Products Table
```
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50)
);
```

# Insert Products Data
```
INSERT INTO products (name, description, price, category) VALUES
('Laptop', 'High-performance laptop with SSD storage', 1200, 'Electronics'),
('Smartphone', 'Latest model with dual-camera setup', 800, 'Electronics'),
('Smart Watch', 'Fitness tracker with heart-rate monitor', 150, 'Electronics'),
('Headphones', 'Noise-canceling wireless headphones', 200, 'Electronics'),
('Men''s Watch', 'Luxury automatic watch with leather strap', 1000, 'Fashion'),
('Women''s Handbag', 'Designer handbag with premium leather', 500, 'Fashion'),
('Sports Shoes', 'Running shoes with breathable mesh', 120, 'Fashion'),
('Backpack', 'Waterproof backpack with laptop compartment', 80, 'Fashion'),
('Blender', 'High-power blender for smoothies', 150, 'Home Appliances'),
('Coffee Maker', 'Programmable coffee maker with thermal carafe', 80, 'Home Appliances'),
('Microwave Oven', 'Countertop microwave oven with cooking presets', 200, 'Home Appliances'),
('Air Purifier', 'HEPA filter air purifier for allergies', 300, 'Home Appliances');
```

# Create Sales Table
```
CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    sale_price DECIMAL(10, 2),
    sale_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Create Random Sales Entry in the table
```
DELIMITER //

CREATE PROCEDURE InsertRandomSale()
BEGIN
    DECLARE product_id INT;
    DECLARE quantity INT;
    DECLARE sale_price DECIMAL(10, 2);

    SET product_id = FLOOR(1 + (RAND() * 12)); -- Random product_id between 1 and 10
    SET quantity = FLOOR(1 + (RAND() * 20)); -- Random quantity between 1 and 5
    SET sale_price = ROUND(10.0 + (RAND() * (1000.0 - 10.0)), 2); -- Random sale_price between 10.0 and 1000.0

    INSERT INTO sales (product_id, quantity, sale_price, sale_timestamp)
    VALUES (product_id, quantity, sale_price, NOW());
END //

DELIMITER ;


SET GLOBAL event_scheduler = ON;


CREATE EVENT InsertSaleEvent
ON SCHEDULE EVERY 1 MINUTE
DO
CALL InsertRandomSale();
```


# Some queries
## top products sold
```
SELECT 
    products.name, 
    COUNT(*) AS sales_count
FROM 
    mydatabase.products 
INNER JOIN 
    mydatabase.sales 
ON 
    products.id = sales.product_id 
GROUP BY 
    products.name;
```

## revenue generated so far
```
SELECT
  sale_timestamp as time,
  SUM(sale_price)
FROM
  mydatabase.sales
GROUP BY time
```
