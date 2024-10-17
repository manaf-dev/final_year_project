import requests

endpoint = "http://localhost:8000"


def get_data():
    response = requests.get(endpoint)
    data = response.json()
    print(data)
