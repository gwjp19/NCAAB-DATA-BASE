import requests
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
  feild_goal_attempts_allowed INTEGER,
  offensive_rebounds_allowed INTEGER,
  total_rebounds_allowed INTEGER,
  turnovers_forced INTEGER,
  fouls_drawn INTEGER,
  PRIMARY KEY (game_id, team_id)
)
""")



url = "https://ncaa-api.henrygd.me/schedule-alt/basketball-men/d1/2026"

response = requests.get(url)
response.raise_for_status()
  

data = response.json()
skipped_games = []

for date_info in data["data"]["schedules"]["games"]:
  date = date_info["contestDate"]
  month, day, year = date.split("/")
  url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{year}/{month}/{day}/all-conf"
  response = requests.get(url)
  response.raise_for_status()
  scoreboard = response.json()
  for game in scoreboard["games"]:
    game_id = game["game"]["gameID"]
    game_id_url = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"
    game_id_response = requests.get(game_id_url)
    if game_id_response.status_code == 502:
      print(f"Skipping game {game_id}: API returned 502")
      skipped_games.append(game_id) 
      continue            
    game_id_response.raise_for_status()
    game_stats = game_id_response.json()      
    for i, team in enumerate(game_stats["teamBoxscore"]):
      team_id = team["teamId"]
      stats = team["teamStats"]
      opponent = game_stats["teamBoxscore"][1-i]["teamStats"]
for game_id in skippied_games:
  game_id_url2 = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"
  game_id_response2 = requests.get(game_id_url2)
  if game_id_response.status_code == 502:
    print(f"Skipping game {game_id}: API returned 502") 
    continue      
  game_id_response2.raise_for_status()
  game_stats2 = game_id_response2.json()
  for i, team in enumerate(game_stats2["teamBoxscore"]):
    team_id = team["teamId"]
    stats = team["teamStats"]
    opponent = game_stats2["teamBoxscore"][1-i]["teamStats"]
      

      
      
    
      
      cursor.execute("""
      INSERT OR REPLACE INTO team_game_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        int(stats["blockedShots"]),
        int(opponent["feildGoalsAttempted"]),
        int(opponent["offensiveRebounds"]),
        int(opponent["totalReboounds"]),
        int(opponent["turnovers"]),
        int(opponent["personalFouls"])
      ))
conection.commit()
conection.close()

print("Finished downloading database")






