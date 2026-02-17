import requests

url = 'http://localhost:8000/process' # Removed trailing slash to match @app.post('/process')
params = {'name': 'NAM8062177 BL.pdf'}

# Use 'params' instead of 'json'
response = requests.post(url, params=params)

print(response.status_code)
print(response.json())