# Create a SQLAlchemy engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///data/db/items.db') 

# Create a SQLAlchemy session 
Session = sessionmaker(bind=engine) 
session = Session() 
