from utils import get_product_price

class CouponCartwise:
    def __init__(self,coupon_details,cart_items):
        self.coupon_details = coupon_details
        self.cart_items = cart_items

    def calculate_discount(self):
        threshold = self.coupon_details.get("threshold")
        discount = self.coupon_details.get("discount")
        # Calculate cart total
        cart_total = sum(item['quantity'] * get_product_price(item['product_id']) for item in self.cart_items)
        if cart_total >= threshold:
            return cart_total * (discount / 100)
        return 0
    
    def apply_discount(self):
        updated_cart = {"items": [], "total_discount": 0, "total_price": 0, "final_price": 0}
         # Apply cart-wise discount to the total cart price
        cart_total = sum(item['quantity'] * get_product_price(item['product_id']) for item in self.cart_items)
        cart_discount = self.calculate_discount()
        updated_cart["total_discount"] = cart_discount
        updated_cart["items"] = self.cart_items
        updated_cart["total_price"] = cart_total
        updated_cart["final_price"] = cart_total - cart_discount
        return updated_cart


class CouponProductWise:
    def __init__(self,coupon_details,cart_items):
        self.coupon_details = coupon_details
        self.cart_items = cart_items

    def calculate_discount(self):
        product_id = self.coupon_details.get("product_id")
        price = get_product_price(product_id)
        discount = self.coupon_details.get("discount")
        # Calculate product-specific discount
        for item in self.cart_items:
            if item['product_id'] == product_id:
                return price * (discount / 100) * item['quantity']
        return 0
    
    def apply_discount(self):
        product_id = self.coupon_details.get("product_id")
        discount = self.coupon_details.get("discount")
        updated_cart = {"items": [], "total_discount": 0, "total_price": 0, "final_price": 0}
        total_discount = 0
        for item in self.cart_items:
            if item['product_id'] == product_id:
                item_discount = get_product_price(item['product_id']) * (discount / 100)
                item['total_discount'] = item_discount * item['quantity']
                item['discounted_price'] = get_product_price(item['product_id']) - item_discount
                total_discount += item['total_discount']
            updated_cart["items"].append(item)
        
        cart_total = sum(item['quantity'] * get_product_price(item['product_id']) for item in self.cart_items)
        updated_cart["total_discount"] = total_discount
        updated_cart["total_price"] = cart_total
        updated_cart["final_price"] = cart_total - total_discount
        return updated_cart


class CouponBxGy:
    def __init__(self,coupon_details,cart_items):
        self.coupon_details = coupon_details
        self.cart_items = cart_items

    def calculate_discount(self):
        get_products = self.coupon_details.get("get_products")
        eligible_repetitions = self.get_eligible_repetitions()
        # Calculate discount for eligible free products
        discount = 0
        for get_product in get_products:
            product_id = get_product['product_id']
            product_price = get_product_price(product_id)
            free_quantity = get_product['quantity'] * eligible_repetitions
            for item in self.cart_items:
                if item['product_id'] == product_id:
                    discount += product_price * min(item['quantity'], free_quantity)
        return discount
    
    def get_eligible_repetitions(self):
        # Apply BxGy discounts
        buy_products = self.coupon_details.get("buy_products")
        repetition_limit = self.coupon_details.get("repition_limit")
        buy_count = 0
        # Calculate eligible repetitions
        for buy_product in buy_products:
            for item in self.cart_items:
                if item['product_id'] == buy_product['product_id']:
                    buy_count += item['quantity'] // buy_product['quantity']

        eligible_repetitions = min(buy_count, repetition_limit)
        return eligible_repetitions


    def apply_discount(self):
        get_products = self.coupon_details.get("get_products")
        eligible_repetitions = self.get_eligible_repetitions()
        free_items = []
        total_discount = 0
        # Mark free items and calculate discount
        updated_cart = {"items": [], "total_discount": 0, "total_price": 0, "final_price": 0}
        for get_product in get_products:
            for item in self.cart_items:
                if item['product_id'] == get_product['product_id']:
                    free_quantity = get_product['quantity'] * eligible_repetitions
                    free_discount = min(free_quantity, item['quantity']) * get_product_price(item['product_id'])
                    item['total_discount'] = free_discount
                    total_discount += free_discount
                    free_items.append(item)
        
        updated_cart["items"] = self.cart_items
        updated_cart["total_discount"] = total_discount
        cart_total = sum(item['quantity'] * get_product_price(item['product_id']) for item in self.cart_items)
        updated_cart["total_price"] = cart_total
        updated_cart["final_price"] = cart_total - total_discount
        return updated_cart
    


def calculate_discount(cart_items,coupon_type, coupon_details):
    """
    Calculate the discount for the given cart based on the coupon details.
    
    Parameters:
        cart_items (list): List of cart items. Each item is a dictionary with keys:
                          - product_id (int)
                          - quantity (int)
                          - price (float)
        coupon_details (dict): Details of the coupon. It should include:
                          - type (str): The type of coupon ("cart-wise", "product-wise", "bxgy").
                          - discount or thresholds based on the type.
    
    Returns:
        float: The total discount applicable for the coupon.
    """
    
    if coupon_type == "cart-wise":
        cart_wise_coupon_obj = CouponCartwise(coupon_details,cart_items)
        cart_wise_discount = cart_wise_coupon_obj.calculate_discount()
        return cart_wise_discount
        
    elif coupon_type == "product-wise":
         product_wise_coupon_obj = CouponProductWise(coupon_details,cart_items)
         product_wise_discount = product_wise_coupon_obj.calculate_discount()
         return product_wise_discount

    elif coupon_type == "bxgy":
        bxgy_coupon_obj = CouponBxGy(coupon_details,cart_items)
        bxgy_wise_discount = bxgy_coupon_obj.calculate_discount()
        return bxgy_wise_discount
    
    # Return 0 if no valid coupon type is matched
    return 0

    


def apply_discount(cart_items,coupon_type, coupon_details):
    """
    Calculate the discount for the given cart based on the coupon details.
    
    Parameters:
        cart_items (list): List of cart items. Each item is a dictionary with keys:
                          - product_id (int)
                          - quantity (int)
                          - price (float)
        coupon_details (dict): Details of the coupon. It should include:
                          - type (str): The type of coupon ("cart-wise", "product-wise", "bxgy").
                          - discount or thresholds based on the type.
    
    Returns:
        float: The total discount applicable for the coupon.
    """
    
    if coupon_type == "cart-wise":
        cart_wise_coupon_obj = CouponCartwise(coupon_details,cart_items)
        updated_cart_items = cart_wise_coupon_obj.apply_discount()
        return updated_cart_items
        
    elif coupon_type == "product-wise":
         product_wise_coupon_obj = CouponProductWise(coupon_details,cart_items)
         updated_cart_items = product_wise_coupon_obj.apply_discount()
         return updated_cart_items

    elif coupon_type == "bxgy":
        bxgy_coupon_obj = CouponBxGy(coupon_details,cart_items)
        updated_cart_items = bxgy_coupon_obj.apply_discount()
        return updated_cart_items
    
    # Return 0 if no valid coupon type is matched
    return 0



