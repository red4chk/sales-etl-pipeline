-- 1. Create the schemas (our Data Warehouse layers)
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS refined;
CREATE SCHEMA IF NOT EXISTS report;

-- 2. Create the raw table to hold our Mockaroo data
CREATE TABLE IF NOT EXISTS raw.sales_transactions (
    transaction_id INT,
    transaction_date VARCHAR(50), 
    customer_id INT,
    customer_first_name VARCHAR(100),
    customer_last_name VARCHAR(100),
    customer_country VARCHAR(100),
    product_id INT,
    product_name VARCHAR(255),
    quantity INT,
    unit_price NUMERIC(10, 2),
    sales_rep_id INT,
    sales_rep_name VARCHAR(255),
    
    -- Metadata column: to track exactly when we pulled this data
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);