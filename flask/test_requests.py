import requests 
import json

addr = 'http://127.0.0.1:5000'

iris_url = addr + '/predict_petal_length_api'
data = {'petal_width': 2}

r = requests.post(iris_url, json=data)

print(r.status_code)
print(r.text)


planet_url = addr + '/upload_file_api'
content_type = 'image/jpeg'

headers = {'content-type': content_type} 

# files = {'file': open('src/app/static/uploads/test_11.jpg', 'rb')}

files = {
    'file1': open('src/app/static/uploads/test_11.jpg', 'rb'),
    'file2': open('src/app/static/uploads/test_14.jpg', 'rb')
    }   
 
r = requests.post(planet_url, files=files)
print(r.status_code)
print(r.text)

# curl -F "file=@src/app/static/uploads/test_11.jpg" http://localhost:5000/upload_file_api