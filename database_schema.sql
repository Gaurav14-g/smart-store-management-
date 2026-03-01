-- Smart Store Management System Database Schema

-- Product Table
CREATE TABLE IF NOT EXISTS product (
    id UUID PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_created_at ON product(created_at DESC);
CREATE INDEX idx_product_name ON product(product_name);

-- Customer Table
CREATE TABLE IF NOT EXISTS customer (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customer_created_at ON customer(created_at DESC);
CREATE INDEX idx_customer_name ON customer(name);
CREATE INDEX idx_customer_phone ON customer(phone);

-- Bill Table
CREATE TABLE IF NOT EXISTS bill (
    id UUID PRIMARY KEY,
    bill_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    user_id INTEGER NOT NULL,
    customer_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(id) ON DELETE CASCADE
);

CREATE INDEX idx_bill_date ON bill(bill_date DESC);
CREATE INDEX idx_bill_user ON bill(user_id);
CREATE INDEX idx_bill_customer ON bill(customer_id);

-- Bill Item Table
CREATE TABLE IF NOT EXISTS bill_item (
    id UUID PRIMARY KEY,
    bill_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bill(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE INDEX idx_bill_item_bill ON bill_item(bill_id);
CREATE INDEX idx_bill_item_product ON bill_item(product_id);

-- Sample Data
INSERT INTO product (id, product_name, price, quantity) VALUES
(gen_random_uuid(), 'Laptop Dell XPS', 1200.00, 10),
(gen_random_uuid(), 'Wireless Mouse', 25.00, 50),
(gen_random_uuid(), 'Mechanical Keyboard', 80.00, 30),
(gen_random_uuid(), 'USB-C Cable', 15.00, 100);

INSERT INTO customer (id, name, phone) VALUES
(gen_random_uuid(), 'John Doe', '1234567890'),
(gen_random_uuid(), 'Jane Smith', '9876543210');
