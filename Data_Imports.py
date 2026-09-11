import requests
game_id = "6534658"

url = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"

response = requests.get(url)

response.raise_for_status()

data = response.json()

#print(data)

for team in data["teamBoxscore"]:
  stats = team["teamStats"]
  print("Team ID:", team["teamID"])
  print(stats)
  print()


