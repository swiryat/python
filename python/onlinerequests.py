import requests



def get_online_currencies():
    host = ""

    response = requests.get(host)

    return response.json().get("data")


currency = get_online_currencies()
print(currency)
