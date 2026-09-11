import requests
import sqlite3

api_url = "https://ncaa-api.henrygd.me"

game_id = 6305900
response = request.get(f"{api_url}/game/{game_id}/team-stats"
                      )

response.raise_for_status()

data = response.json()

print(data)
