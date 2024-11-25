
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Boolean, ForeignKey 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
import datetime
import hashlib
import db



# Define a SQLAlchemy model 
Base = declarative_base() 


class Product(Base): 
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True) 
	name = Column(String) 
	price = Column(Float)
	category = Column(String)
	is_ignore = Column(Boolean,default=False)


class Coupons(Base): 
	__tablename__ = 'coupons'
	id = Column(Integer, primary_key=True) 
	type = Column(String) 
	details = Column(JSON)
	coupon_hash = Column(String)
	expiration_date = Column(DateTime)
	created_date = Column(DateTime,default = datetime.datetime.now())
	is_ignore = Column(Boolean,default=False)


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	username = Column(String)
	password = Column(String)
	is_ignore = Column(Boolean,default=False)


class Carts(Base):
	__tablename__ = 'carts'
	id = Column(Integer, primary_key=True) 
	details = Column(JSON)
	user_id = Column(ForeignKey(User.id))
	is_ignore = Column(Boolean,default=False)


Base.metadata.create_all(db.engine) 
	
