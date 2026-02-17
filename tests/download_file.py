import requests

url = 'http://localhost:8000/download/NAM8062177 BL.pdf'
response = requests.get(url)

# Check if the request was successful (Status Code 200)
if response.status_code == 200:
    # Open a local file in write-binary mode
    with open('downloaded_file.pdf', 'wb') as f:
        f.write(response.content)
    print("File saved successfully!")
else:
    print(f"Failed to download file. Status code: {response.status_code}")