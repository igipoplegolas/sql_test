from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Sequence
from sqlalchemy import func
from sqlalchemy.types import *

# create engine to postgres database
engine = create_engine('postgresql://postgres:gizzzmo@localhost:5432/postgres', echo=True);

# bind metadata with engine
metadata = MetaData(bind=engine)

# create surrogate sequence
seq_surrogate_key = Sequence('seq_surrogate_key', metadata=metadata)

# define dimension table dim_customers
dim_customers = Table('dim_customers', metadata,
	Column('surrogate_key', Integer, Sequence('seq_surrogate_key'), primary_key=True),
	Column('id', Integer),
	Column('name', String),
	Column('address', String),
	Column('from_date', Date, default=func.current_date),
	Column('to_date', Date)
);

# create database connection
conn = engine.connect();

# drop dimenstion table and its surrogate key sequence
conn.execute("DROP TABLE IF EXISTS dim_customers");
conn.execute("DROP SEQUENCE IF EXISTS seq_surrogate_key");

# create all tables
metadata.create_all();