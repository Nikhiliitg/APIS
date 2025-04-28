import requests

url = "http://127.0.0.1:5000/request-api-key"
data = {"username": "john_doe"}
response = requests.post(url, json=data)
print(response.json())