from typing import Union
from models import Coupons as Coupon,User
from pydantic import BaseModel, Json
from fastapi import FastAPI
from datetime import datetime
from typing import Any,List 
from services import calculate_discount,apply_discount
import uvicorn
import os
import db 
import hashlib
import json
from utils import *



app = FastAPI()



class CouponSchema(BaseModel):
    type : str
    details : Json[Any]
    expiration_date : datetime
    created_date : datetime

class CartSchema(BaseModel):
    items : Json[Any]

class UserSchema(BaseModel):
    name : str
    username : str
    password : str



@app.post("/coupons")
def create_coupon(coupon: CouponSchema):
    coupon_hash = get_hash(json.dumps(coupon.details))
    coupon_hash_query = db.session.query(Coupon.coupon_hash)
    if coupon_hash in [i[0] for i in coupon_hash_query.all()]:
        return {"message": "Coupon Already Exist", "coupon": coupon}, 404
    new_coupon = Coupon(type=coupon.type,details=coupon.details, expiration_date = coupon.expiration_date,coupon_hash = coupon_hash)
    db.session.add(new_coupon)
    db.session.commit()
    return {"message": "Coupon created", "coupon": coupon}


@app.post("/add_user")
def add_user(user: UserSchema):
    username_query = db.session.query(User.username)
    if user.username in username_query.all():
        return {"message": f"user with username {user.username} already exist"}
    hash_pwd = get_hash(user.password)
    new_user = User(name=user.name,username=user.username, password = hash_pwd)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "user created", "user": user.username}


@app.get("/coupons")
def get_coupons():
    coupons = db.session.query(Coupon)
    return {"coupons": [c for c in coupons.all()]}


@app.post("/applicable-coupons")
def get_applicable_coupons(cart: CartSchema):
    applicable_coupons = []
    coupons = db.session.query(Coupon)
    for coupon in coupons.all():
        # print(cart.items, coupon.details)
        if coupon.expiration_date.date()>=datetime.now().date():
            discount = calculate_discount(cart.items, coupon.type,coupon.details)
            if discount > 0:
                applicable_coupons.append({"coupon_id": coupon.id, "type": coupon.type, "discount": discount})
    return {"applicable_coupons": applicable_coupons}


@app.post("/apply-coupon/{id}")
def apply_coupon(coupon_id: int, cart: CartSchema):
    coupon = [c for c in db.session.query(Coupon).all() if c.id == coupon_id]
    if not coupon:
        return {"error": "Coupon not found"}, 404
    if coupon[0].expiration_date.date() >= datetime.now().date():
        discount = calculate_discount(cart.items, coupon[0].type, coupon[0].details)
        updated_cart = apply_discount(cart.items,coupon[0].type, coupon[0].details)
        return {"updated_cart": updated_cart, "total_discount": discount}
    else:
        return {'message':'Coupon Expired'}



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5002)
    os.system('echo "Coupon Service is up and running"')








