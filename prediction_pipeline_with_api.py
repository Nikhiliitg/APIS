import requests

url = "http://127.0.0.1:5000/predict"
headers = {
    "x-api-key": input("Enter your API key: ")
}
data = {"features": [5.1, 9, 1.4, 0.2]}
response = requests.post(url, json=data, headers=headers)
print(response.json())