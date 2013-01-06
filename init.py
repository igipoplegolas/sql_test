from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy.types import *

# create engine to postgres database
engine = create_engine('postgresql://postgres:gizzzmo@localhost:5432/postgres', echo=True);

# bind metadata with engine
metadata = MetaData(bind=engine)

# define source table src_customers
src_customers = Table('src_customers', metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String),
	Column('address', String)
);

# create all tables
metadata.drop_all();
metadata.create_all();

# create database connection
conn = engine.connect();

# init table with some records
conn.execute(src_customers.insert(), [
	{"id": 1, "name": 'Danko', "address": 'Vavilovova'},
	{"id": 2, "name": 'Stivi', "address": 'Vavilovova'},
	{"id": 3, "name": 'Kotvi', "address": 'Kapicova'}	
]);

# list all records in src_customers
for row in conn.execute(src_customers.select()):
	print row;