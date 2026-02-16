import requests

url = 'http://localhost:8000/delete/test.txt'
response = requests.delete(url)
print(response.json())