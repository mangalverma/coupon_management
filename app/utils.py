import hashlib
from models import Coupons as Coupon,Product
import db

def get_hash(text):
    return hashlib.md5(text.encode()).hexdigest()


def get_product_price(product_id):
        products = db.session.query(Product)
        for p in products.all():
            if p.id == product_id:
                return p.price
        return None
