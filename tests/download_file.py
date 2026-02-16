import requests

url = 'http://localhost:8000/download/test.txt'
response = requests.get(url)
print(response.content)