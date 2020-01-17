import requests 
import json

data = json.dumps({'petal_width': 2})

url = 'http://localhost:5000/predict_api'
r = requests.post(url, json=data)

print(r.status_code)
print(r.text)