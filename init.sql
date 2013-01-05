-- create src_customers table
DROP TABLE IF EXISTS src_customers;

CREATE TABLE src_customers (
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR,
    address VARCHAR
);

-- load some record into src_customers
INSERT INTO src_customers VALUES
    (1, 'Danko', 'Vavilovova'), 
    (2, 'Kotvi', 'Kapicova'),
    (3, 'Stivi', 'Vavilovova');

-- show inserted record
SELECT * FROM src_customers;