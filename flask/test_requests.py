import os 
import json
import requests 
from flask import jsonify

addr = 'http://localhost:5000'

# print(os.getenv('IN_CONTAINER'))
# if os.getenv('IN_CONTAINER'):
#     addr = addr[:-5]

planet_url = addr + '/upload_image_api'

files = [
    ('file', open('data/raw/test-jpg/test_11.jpg', 'rb')),
    ('file', open('data/raw/test-jpg/test_14.jpg', 'rb'))
    ]

r = requests.post(planet_url, files=files)

print(r.text)
print(r.status_code)

r = requests.post(addr+'/predict_petal_length_api', data={'petal_width': 1})
print(r.text)

# curl -F "file=@data/raw/test-jpg/test_11.jpg" http://localhost:5000/upload_image_api
