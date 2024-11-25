
---

# Coupons Management API

A RESTful API to manage and apply discount coupons for an e-commerce platform. This API is designed to handle various types of coupons, including **cart-wise**, **product-wise**, and **BxGy (Buy X Get Y)** coupons. It is extendable for adding new coupon types in the future.

---

## Features

- **Cart-wise Coupons**: Apply discounts to the entire cart if the total value exceeds a threshold.
- **Product-wise Coupons**: Apply discounts to specific products in the cart.
- **BxGy Coupons**: Implement "Buy X, Get Y Free" deals with customizable conditions and repetition limits.
- **CRUD operations** for managing coupons.
- Fetch and apply applicable coupons for a given cart.
- Designed for future extensibility to add new coupon types.
- Includes error handling, documentation, and unit tests.

---

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite (file-based)
- **Language**: Python
- **Tools**: Docker, Postman
- **Testing**: Pytest
- **Other**: JSON for structured data exchange

---

## Setup Instructions

### **1. Prerequisites**
- Python 3.8+
- Docker and Docker Compose (for containerization)
- Postman (optional, for testing API endpoints)

### **2. Installation**

#### **Clone the Repository**
```bash
git clone https://github.com/mangalverma/coupon_management.git
cd coupon_management
```

#### **Run Locally**
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   uvicorn main:app --reload
   ```
4. Open your browser or Postman:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

#### **Run with Docker**
1. Build the Docker image:
   ```bash
   docker-compose up --build
   ```
2. Access the API:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints

### **Coupon Management**
| Method | Endpoint       | Description                  |
|--------|----------------|------------------------------|
| POST   | `/coupons`     | Create a new coupon          |
| GET    | `/coupons`     | Retrieve all coupons         |
| GET    | `/coupons/{id}`| Retrieve a specific coupon   |


### **Coupon Application**
| Method | Endpoint                | Description                      |
|--------|-------------------------|----------------------------------|
| POST   | `/applicable-coupons`   | Fetch applicable coupons for a cart |
| POST   | `/apply-coupon/{id}`    | Apply a specific coupon to a cart |

---

## Coupon Types

### **1. Cart-wise Coupons**
- **Description**: Discount applied to the entire cart if the total exceeds a threshold.
- **Example**:
  ```json
  {
    "type": "cart-wise",
    "details": {
      "threshold": 100,
      "discount": 10
    }
  }
  ```

### **2. Product-wise Coupons**
- **Description**: Discount applied to a specific product.
- **Example**:
  ```json
  {
    "type": "product-wise",
    "details": {
      "product_id": 1,
      "discount": 20
    }
  }
  ```

### **3. BxGy Coupons**
- **Description**: "Buy X, Get Y" coupons with repetition limits.
- **Example**:
  ```json
  {
    "type": "bxgy",
    "details": {
      "buy_products": [
        {"product_id": 1, "quantity": 3}
      ],
      "get_products": [
        {"product_id": 3, "quantity": 1}
      ],
      "repition_limit": 2
    }
  }
  ```

---

## Testing

### **Postman**
1. Import the `coupon_management/postman_API/api.json` provided in the repository.
2. Use pre-configured requests to test the API.

---

## Limitations

1. **Concurrency**: The current SQLite implementation may not handle high levels of concurrency.
2. **Coupon Stacking**: Coupons cannot be stacked (only one coupon is applied per cart).
3. **Validation**: Complex validations (e.g., user-specific coupons) are not implemented.

---

## Future Improvements

1. **Support Coupon Stacking**: Implement rules to allow multiple coupons.
2. **User-Specific Coupons**: Add user targeting for personalized coupons.
3. **Advanced Logging**: Enhance logging for better debugging and analytics.

---

## License
This project is licensed under the MIT License.

---

Copy and save the above content as `README.md` in your project directory. Let me know if you need further customization or help!
