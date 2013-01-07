-- update data in dim_customers from src_customers

-- insert new records and make them active (to_date is null)
INSERT INTO dim_customers (id, name, address)
	SELECT src.* FROM src_customers src
	JOIN (
		SELECT id FROM src_customers
		EXCEPT 
		SELECT id FROM dim_customers	
	) tmp ON src.id = tmp.id;


-- update changed records
DROP TABLE IF EXISTS diff_customers;

-- find last active record with data to be updated
CREATE TABLE diff_customers AS (
	SELECT DISTINCT src.* 
	FROM src_customers src
	JOIN dim_customers dim 
	ON src.id = dim.id
	WHERE (src.name != dim.name OR src.address != dim.address) AND dim.to_date IS NULL
);

-- make the last active record inactive (set to_date to current date)
UPDATE dim_customers dim
	SET to_date = CURRENT_DATE 
	FROM diff_customers diff 
	WHERE dim.id = diff.id AND dim.to_date IS NULL;

-- insert new active record with updated data
INSERT INTO dim_customers (id, name, address) 
	SELECT * FROM diff_customers;