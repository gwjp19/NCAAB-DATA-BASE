import requests
import sqlite3
from datetime import datetime

conection = sqlite3.connect("basketball.db")
cursor = conection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS team_game_stats (
  game_id INTEGER,
  team_id INTEGER,
  points INTEGER,
  field_goals_made INTEGER,
  field_goals_attempted INTEGER,
  three_points_made INTEGER,
  three_points_attempted INTEGER,
  free_throws_made INTEGER,
  free_throws_attempted INTEGER,
  offensive_rebounds INTEGER,
  total_rebounds INTEGER,
  assists INTEGER,
  turnovers INTEGER,
  personal_fouls INTEGER,
  steals INTEGER,
  blocked_shots INTEGER,
  field_goal_attempts_allowed INTEGER,
  offensive_rebounds_allowed INTEGER,
  total_rebounds_allowed INTEGER,
  turnovers_forced INTEGER,
  fouls_drawn INTEGER,
  ppp FLOAT,
  papp FLOAT,
  PRIMARY KEY (game_id, team_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS teams (
  team_id INTEGER PRIMARY KEY,
  team_name TEXT NOT NULL
  )
""")
# convert every needed stat to int once 
NEEDED = [
    "fieldGoalsMade", "fieldGoalsAttempted",
    "threePointsMade", "threePointsAttempted",
    "freeThrowsMade", "freeThrowsAttempted",
    "offensiveRebounds", "totalRebounds",
    "assists", "turnovers", "personalFouls",
    "steals", "blockedShots",
]

def clean(raw):
    return {k: int(raw[k]) for k in NEEDED}

def pts(s):
    return 2 * s["fieldGoalsMade"] + s["threePointsMade"] + s["freeThrowsMade"]

def poss(s):
    return (s["fieldGoalsAttempted"] - s["offensiveRebounds"]
            + 0.475 * s["freeThrowsAttempted"] + s["turnovers"])

def process_game(game_id):
    """Returns True if saved, False if the game should be skipped/retried."""
    game_id_url = f"https://ncaa-api.henrygd.me/game/{game_id}/team-stats"
    game_id_response = requests.get(game_id_url)
    if game_id_response.status_code == 502:
        print(f"Skipping game {game_id}: API returned 502")
        return False
    game_id_response.raise_for_status()
    game_stats = game_id_response.json()
    game_response = requests.get(f"https://ncaa-api.henry.gd.me/game/{game_id}")
    game_response.raise_for_status()
    game_data = game_response.json()

    for team in game_data["contests"][0]["teams"]:
      cursor.execute("""
        INSERT OR REPLACE INTO TEAMS (team_id, team_name)
        VALUES (?, ?)
      """, (
        int(team["teamId"])
        team["nameFull"]
      ))

    rows = []
    try:
        for i, team in enumerate(game_stats["teamBoxscore"]):
            stats = clean(team["teamStats"])
            opponent = clean(game_stats["teamBoxscore"][1 - i]["teamStats"])
            ppp = pts(stats) / poss(stats)
            papp = pts(opponent) / poss(opponent)
            rows.append((
                int(game_id),
                int(team["teamId"]),
                pts(stats),
                stats["fieldGoalsMade"],
                stats["fieldGoalsAttempted"],
                stats["threePointsMade"],
                stats["threePointsAttempted"],
                stats["freeThrowsMade"],
                stats["freeThrowsAttempted"],
                stats["offensiveRebounds"],
                stats["totalRebounds"],
                stats["assists"],
                stats["turnovers"],
                stats["personalFouls"],
                stats["steals"],
                stats["blockedShots"],
                opponent["fieldGoalsAttempted"],
                opponent["offensiveRebounds"],
                opponent["totalRebounds"],
                opponent["turnovers"],
                opponent["personalFouls"],
                ppp,
                papp,
            ))
    except (KeyError, ValueError, ZeroDivisionError) as e:
        print(f"Skipping game {game_id}: bad data ({e!r})")
        return False

    # only write once both teams parsed cleanly
    for row in rows:
        cursor.execute(
            "INSERT OR REPLACE INTO team_game_stats VALUES ("
            + ",".join("?" * 23) + ")",
            row,
        )
    return True

url = "https://ncaa-api.henrygd.me/schedule-alt/basketball-men/d1/2026"
response = requests.get(url)
response.raise_for_status()
data = response.json()

skipped_dates = []
skipped_games = []

# unique dates, sorted chronologically
all_games = data["data"]["schedules"]["games"]
dates = sorted(
    {g["contestDate"] for g in all_games},
    key=lambda d: datetime.strptime(d, "%m/%d/%Y"),
)

for date in dates:
    month, day, year = date.split("/")
    month, day = month.zfill(2), day.zfill(2)
    url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{year}/{month}/{day}/all-conf"
    response = requests.get(url)
    if response.status_code == 502:
        print(f"API returned 502, skipping date {date}")
        skipped_dates.append(date)
        continue
    response.raise_for_status()
    scoreboard = response.json()
    for game in scoreboard["games"]:
        game_id = game["game"]["gameID"]
        if not process_game(game_id):
            skipped_games.append(game_id)
    conection.commit()  # save after each date so a crash doesn't lose everything

# retry skipped dates
for date in skipped_dates:
    month, day, year = date.split("/")
    month, day = month.zfill(2), day.zfill(2)
    url = f"https://ncaa-api.henrygd.me/scoreboard/basketball-men/d1/{year}/{month}/{day}/all-conf"
    response = requests.get(url)
    if response.status_code == 502:
        print(f"Date {date}: API still unresponsive")
        continue
    response.raise_for_status()
    for game in response.json()["games"]:
        game_id = game["game"]["gameID"]
        if not process_game(game_id):
            skipped_games.append(game_id)

# retry skipped games
for game_id in skipped_games:
    if not process_game(game_id):
        print(f"{game_id}: still failing")

conection.commit()
conection.close()

print("Finished downloading database")
