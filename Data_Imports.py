import requests
import sqlite3

api_url = "https://ncaa-api.henrygd.me"

game_id = 6305900
response = requests.get(f"{api_url}/game/{game_id}/team-stats"
                      )

response.raise_for_status()

data = response.json()

print(data)

url = "https://ncaa-api.henrygd.me/schedule/basketball-men/d1/2025/02"

response2 = requests.get(url)

response2.raise_for_status()

data2 = response2.json()

print(data2)
