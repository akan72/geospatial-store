import os 
import json
import requests 

addr = 'http://localhost:5000'
print(os.getenv('IN_CONTAINER'))


if os.getenv('IN_CONTAINER'):
    addr = addr[:-5]

planet_url = addr + '/upload_image_api'

files = {
    'file1': open('data/raw/test-jpg/test_11.jpg', 'rb'),
    'file2': open('data/raw/test-jpg/test_14.jpg', 'rb')
    }   
 
r = requests.post(planet_url, files=files)
print(r.text)

r = requests.post(addr + '/predict_petal_length_api', data={'petal_width': 1})
print(r.text)
 
# curl -F "file=@data/raw/test-jpg/test_11.jpg" http://localhost:5000/upload_file_api