import requests
import pandas as pd
import json
import db 
from models import Coupons as Coupon,User,Product
from utils import get_hash
from datetime import datetime

coupons_df = pd.read_csv("../data/dummy_data/coupons.csv - coupons.csv")
for i,row in coupons_df.iterrows():
    coupon_hash = get_hash(row['details'])
    new_coupon = Coupon(type=row['type'],details=json.loads(row['details']), expiration_date = datetime.strptime(row["expiration_date"],"%Y-%m-%d"), coupon_hash = coupon_hash )
    db.session.add(new_coupon)
    db.session.commit()



user_df = pd.read_csv("../data/dummy_data/coupons.csv - users.csv")
for i,row in user_df.iterrows():
    new_user = User(name=row['user'], username=row['username'], password = row["password"])
    db.session.add(new_user)
    db.session.commit()

product_df = pd.read_csv("../data/dummy_data/coupons.csv - product.csv")
for i,row in product_df.iterrows():
    new_product = Product(name = row['name'], price = row['price'], category = row['category'])
    db.session.add(new_product)
    db.session.commit()
    


