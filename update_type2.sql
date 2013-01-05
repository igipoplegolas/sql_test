-- update data in dim_customers from src_customers

-- insert new records
SELECT src.id FROM src_customers src EXCEPT SELECT dim.id FROM dim_customers dim;