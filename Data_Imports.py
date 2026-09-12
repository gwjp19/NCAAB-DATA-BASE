import requests
game_id = []

url = f"https://ncaa-api.henrygd.me/schedule-alt/basketball-men/d1/2026"
  

#url = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"

response = requests.get(url)

response.raise_for_status()

data = response.json()

print(type(data))
print(data.keys())

#for month in range (1,4):
  #url = f"https://ncaa-api.henrygd.me/schedule/basketball-men/d1/2025/{month:02d}"
  
  #response = requests.get(url)

  #response.raise_for_status()

  #data = response.json()


print(data)

for date in data["dates"]:
  print(date["contestDate"])

for team in data["teamBoxscore"]:
  stats = team["teamStats"]
  print("Team ID:", team["teamId"])
  print(stats)
  print()

import sqlite3

conection = sqlite3.connect("basketball.db")
cursor = conection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS team_game_stats (
  game_id INTEGER,
  team_id INTEGER,
  feild_goals_made INTEGER, 
  feild_gaols_attempted INTEGER,
  three_points_made INTEGER,
  three_points_attempted INTEGER,
  free_throws_made INTEGER,
  free_throws_attempted INTERGER,
  offensive_rebounds INTEGER, 
  total_renounds INTEGER,
  assists INTEGER,
  turnovers INTEGER,
  personal_fouls INTEGER,
  steals INTEGER,
  blocked_shots INTEGER,
  PRIMARY KEY (game_id, team_id)
)
""")
for team in data["teamBoxscore"]:
  stats = team["teamStats"]

  cursor.execute("""
  INSERT OR REPLACE INTO team_game_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  """, (
    int(game_id),
    int(team["teamId"]),
    int(stats["fieldGoalsMade"]),
    int(stats["fieldGoalsAttempted"]),
    int(stats["threePointsMade"]),
    int(stats["threePointsAttempted"]),
    int(stats["freeThrowsMade"]),
    int(stats["freeThrowsAttempted"]),
    int(stats["offensiveRebounds"]),
    int(stats["totalRebounds"]),
    int(stats["assists"]),
    int(stats["turnovers"]),
    int(stats["personalFouls"]),
    int(stats["steals"]),
    int(stats["blockedShots"])
  ))
conection.commit()
conection.close()

print("Game Imported Into Database!")


  
