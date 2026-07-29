-- Create database
CREATE DATABASE company_cs;

-- Create orders table
CREATE EXTERNAL TABLE company_cs.orders (
    order_id STRING,
    customer_id STRING,
    customer_name STRING,
    product STRING,
    quantity INT,
    price DOUBLE,
    order_date STRING,
    status STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://company-cs-agent/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Create shipments table
CREATE EXTERNAL TABLE company_cs.shipments (
    shipment_id STRING,
    order_id STRING,
    carrier STRING,
    tracking_number STRING,
    ship_date STRING,
    estimated_delivery STRING,
    status STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LOCATION 's3://company-cs-agent/'
TBLPROPERTIES ('skip.header.line.count'='1');