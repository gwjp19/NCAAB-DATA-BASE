import requests
#url = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"


url = "https://ncaa-api.henrygd.me/schedule-alt/basketball-men/d1/2026"

response = requests.get(url)
response.raise_for_status()
  

data = response.json()

for date_info in data["data"]["schedules"]["games"]:
  date = date_info["contestDate"]
  month, day, year = date.split("/")
  url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{year}/{month}/{day}/all-conf"
  response = requests.get(url)
  response.raise_for_status()
  scoreboard = response.json()
  
  for game in scoreboard["games"]:
    game_id = game["game"]["gameId"]
    print(game_id)


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


  
