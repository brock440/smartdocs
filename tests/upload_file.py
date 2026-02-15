import requests
import json 

url = 'http://localhost:8000/upload'
files = {'file': open('test.txt', 'r')}

data = {
    'name': 'test.txt',
    'file_type': 'text',
    'file_size': 100,
    'file_hash': '1234567890',
}
response = requests.post(url, data=data, files=files)
print(response.json())