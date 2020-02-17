import requests 
import json

data = {'petal_width': 2}

url = 'http://127.0.0.1/predict_api'
r = requests.post(url, json=data)

print(r.status_code)
print(r.text)