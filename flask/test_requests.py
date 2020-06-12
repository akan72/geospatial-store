import os 
import json
import requests 

files = [
    ('file', open('data/raw/test-jpg/test_11.jpg', 'rb')),
    ('file', open('data/raw/test-jpg/test_14.jpg', 'rb'))
    ]

addr = 'http://localhost'   
planet_url = addr + '/upload_image_api'
r = requests.post(planet_url, files=files)

print(r.text)
print(r.status_code)

# curl -F "file=@data/raw/test-jpg/test_11.jpg" http://localhost/upload_image_api
