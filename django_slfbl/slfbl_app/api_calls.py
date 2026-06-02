# File to act as a bridge between the API calls and the impementation.
# If the API calls change, this is the only file that should need to be updated.

import statsapi

# Get the schedule of games for the given date range.
# Returns a list of games, where each game is a dictionary containing information about the game.
# start_date and end_date should be in the format 'MM/DD/YYYY'.
#
# The return value is expected to be a list of dictionaries, where each dictionary
# contains information about a game and must include the following values:
# - 'game_id': The unique ID of the game as a number.
# - 'game_date': The date of the game in the format 'YYYY-MM-DD' as a string.
def getGames(start_date, end_date):
    return statsapi.schedule(start_date=start_date, end_date=end_date)

# Get the boxscore data for a given game ID.
# Returns a dictionary containing information about the game, including the players who played, their stats, etc.
#
# The return value is expected to be a dictionary containing information about the game, including the players who played, their stats, etc.
# The dictionary should include the following values:
# - 'playerInfo': A dictionary where the keys are player IDs and the values are dictionaries containing information about the player:
#   - 'fullName': The full name of the player as a string.
# - 'away': A dictionary containing information about the away team:
#   - 'batters': A list of player IDs representing the players who batted for the away team in the game.
#   - 'pitchers': A list of player IDs representing the players who pitched for the away team in the game.
#   - 'players': A list of dictionaries where the keys are player IDs (formatted 'ID<player_id>') and the values are dictionaries containing information about the player's performance in the game:
#     - 'allPositions': A list of dictionaries representing the positions the player played in the game with a key of 'abbreviation' and a value which is the position abbreviation as a string.
#     - 'stats': A dictionary containing the stats:
#       - 'batting': A dictionary containing the batting stats:
#         - 'hits': The number of hits the player had in the game as a number.
#         - 'rbi': The number of RBIs the player had in the game as a number.
#         - 'runs': The number of runs the player scored in the game as a number.
#         - 'stolenBases': The number of stolen bases the player had in the game as a number.
#       - 'pitching': A dictionary containing the pitching stats:
#         - 'inningsPitched': The number of innings the player pitched in the game as a number.
#         - 'wins': The number of wins the player had in the game as a number.
#         - 'runs': The number of runs the player allowed in the game as a number.
#         - 'earnedRuns': The number of earned runs the player allowed in the game as a number.
#         - 'hits': The number of hits the player allowed in the game as a number.
#         - 'note': Contains 'S' if the player got a save in the game, otherwise is an empty string.
#         - 'holds': The number of holds the player had in the game as a number.
#         - 'losses': The number of losses the player had in the game as a number.
#         - 'blownSaves': The number of blown saves the player had in the game as a number.
# - 'home': A dictionary containing information about the home team, with the same structure as the 'away' dictionary.
def getBoxscoreData(game_id):
    return statsapi.boxscore_data(game_id)