import requests

url = "https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1"

response = requests.get(url)

response.raise_for_status()

data = response.json()

print(data)
