import requests

url = "http://127.0.0.1:5000/approve-api-key"
data = {
    "admin_secret": "Nikhil0007@",
    "username": "john_doe"
}
response = requests.post(url, json=data)
print(response.json())
# {'username': 'john_doe', 'api_key': 'generated-api-key'}
