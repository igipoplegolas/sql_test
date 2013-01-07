-- create dim_customers table
DROP TABLE IF EXISTS dim_customers;

-- create sequence for dim_customers surrogate key
DROP SEQUENCE IF EXISTS seq_surrogate_key;
CREATE SEQUENCE seq_surrogate_key;

CREATE TABLE dim_customers (
	surrogate_key INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('seq_surrogate_key'),
	id INTEGER NOT NULL,
	name VARCHAR,
	address VARCHAR,
	from_data DATE NOT NULL DEFAULT CURRENT_DATE,
	to_date DATE
);