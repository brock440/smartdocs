import requests
import json
import hashlib


url = 'http://localhost:8000/upload'
files = {'file': open(r"C:\Users\Bhargav Joshi\Downloads\NAM8062177 BL.pdf", 'rb')}
file_hash = hashlib.sha256(files['file'].read()).hexdigest()
files['file'].seek(0)
data = {
    'name': 'test.txt',
    'file_type': 'text',
    'file_size': 100,
    'file_hash': file_hash,
}
response = requests.post(url, data=data, files=files)
print(response.json())