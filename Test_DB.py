import sqlite3
conection = sqlite3.conect("basketball.db")
cursor = conection.cursor()

cursor.execute("SELECT * FROM team_game_stats")
rows = cursor.fetchall()

for row in rows:
  print(row)

conection.close()
