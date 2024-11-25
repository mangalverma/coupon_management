import requests
import json


# d = {
#   "type": "product-wise",
#   "details": "{\"product_id\":1,\"\":10}",
#   "expiration_date": "2025-11-23T15:53:01.906Z",
#   "created_date": "2024-11-23T15:53:01.906Z"
# }
# res = requests.post("http://127.0.0.1:5002/coupons" ,headers= {'Content-type': 'application/json'}, data = json.dumps(d) )
# print(res.json())


d = {
  "type": "product-wise",
  "details": "{\"product_id\":1,\"discount\":20}",
  "expiration_date": "2025-11-23T15:53:01.906Z",
  "created_date": "2024-11-23T15:53:01.906Z"
}
res = requests.post("http://127.0.0.1:5002/coupons" ,headers= {'Content-type': 'application/json'}, data = json.dumps(d) )
print(res.json())