from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import sql
from sqlalchemy import and_
from sqlalchemy import or_

engine = create_engine("postgresql://postgres:postgres@localhost/test_db")
metadata = MetaData(bind=engine)

# create and load tables
src_customers = Table("src_customers", metadata, autoload=True)
dim_customers = Table("dim_customers", metadata, autoload=True)


def insert_new(src_table, dim_table):
	"""Insert new records"""

	# get table ids
	src_id = sql.select([src_table.c.id], from_obj=src_table)
	dim_id = sql.select([dim_table.c.id], from_obj=dim_table)

	# create diff ids
	diff = src_id.except_(dim_id)

	# create alias for diff ids
	diff_alias = sql.Alias(diff, "diff")

	# join tables based on diff ids
	joined_table = src_table.join(diff_alias, src_table.c.id == diff_alias.c.id)
	
	# get records from source with diff ids
	new_records = sql.select(src_table.c, from_obj=joined_table)

	# insert new records into dim table
	for row in new_records.execute():
		engine.execute(dim_table.insert(), row)
		print "Inserting row", str(row)

def update_changed(src_table, dim_table):
	"""Update changed records"""

	# create condition
	where_clause = and_(or_(src_table.c.name != dim_table.c.name, src_table.c.address != dim_table.c.address), dim_table.c.to_date == None)

	# join table based on their ids
	joined_table = src_table.join(dim_table, src_table.c.id == dim_table.c.id)

	# create statement for table with only changed records
	change_table = sql.select(src_table.c, whereclause=where_clause, from_obj=joined_table)

	# update records in dim table and create new records
	for row in change_table.execute():
		# create condition
		where_clause = and_(dim_table.c.id == row.id, dim_table.c.to_date == None)

		# create current timestamp
		timestamp = sql.functions.current_timestamp()

    	# update record
		sql.update(dim_table, whereclause=where_clause, values={dim_table.c.to_date:timestamp}).execute()
		print "Updating row", str(row)

    	# insert record
		engine.execute(dim_table.insert(), row)
    

if __name__ == "__main__":
	insert_new(src_customers, dim_customers)
	update_changed(src_customers, dim_customers)