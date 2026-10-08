# NCAAB-DATA-BASE

## Database Design

The database is an SQLite database built using data provided from the NCAA-API from Henrygd. The API is run locally to ensure reliable connection and optimal performance. The database cleans and structures the data to ensure complete rows and consistent formatting.

### Team Table:

The team table links team names and team IDs, making it easy to switch between names and IDs when querying the database.

### Game_Stats Table

Multiple features are calculated and stored for each teams performance in each game, including:

-Points

-Possessions

-Field Goals Made/Attempted

-Three Pointers Made/Attempted

-Free Throws Made/Attempted

-Offensive and total rebounds

-Assists 

-Turnovers/Turnovers Forced

-Personal Fouls/Fouls Drawn

-Steals

-Blocked Shots

-Field Goal Attempts Allowed

-Offensive and Total Rebounds Allowed

-Points Per Possession and Points Allowed Per Possession

These features are calculated for each teaming every game. The database import the data from the API, processes it, and stores the resulting statuses rows in the database.

