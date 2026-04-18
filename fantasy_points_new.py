import statsapi
import json
import csv
from datetime import date, datetime
from time import sleep
from user_input import *


longestPlayerName = 0
gameDates = []
boxscoreDatas = {}
games = statsapi.schedule(start_date=start_date, end_date=end_date)
startDate = datetime.strptime(start_date, '%m/%d/%Y')
endDate = datetime.strptime(end_date, '%m/%d/%Y')
numWeeks = (endDate - startDate).days / 7
playerPositions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']
playerTeams = {}

# This function calls the API to download the boxscores,
# saves the data in boxscoreDatas variable and writes
# the data to boxscores.json file
def downloadScores():
    print('Downloading boxscores...', end='')
    global boxscoreDatas
    boxscoreDatas = {}
    _boxscoreDatas = {}
    for game in games:
        _boxscoreDatas[game['game_id']] = statsapi.boxscore_data(game['game_id'])
        print('.', end="")
    # Saving boxscore data
    with open("boxscores.json", "w") as outfile:
        boxscoreDatas = json.loads(json.dumps(_boxscoreDatas))
        json.dump(_boxscoreDatas, outfile)
    print('\nBoxscores saved.')

# This function reads the boxscores.json file to load the boxscores,
# and saves the data in boxscoreDatas variable
def loadScores():
    print('Loading boxscores...')
    global boxscoreDatas
    boxscoreDatas = {}
    # Opening boxscores file
    with open('boxscores.json', 'r') as openfile:
        # Reading from json file
        boxscoreDatas = json.load(openfile)
    print('Boxscores loaded.')

def findDatesAndBoxscores():
    if mode == 'weekly':
        for game in games:
            if game['game_date'] not in gameDates:
                gameDates.append(game['game_date'])
    if doDownloadScores:
        downloadScores()
    else:
        loadScores()

def determineLongestPlayerName(doubleArrayOfNames):
    global longestPlayerName
    longestPlayerName = 0
    for arrayOfNames in doubleArrayOfNames:
        for playerName in arrayOfNames:
            if len(playerName) > longestPlayerName:
                longestPlayerName = len(playerName)

def calculateBatterPoints(playerStats):
    if not playerStats:
        return 0, 0
    points = playerStats['hits'] + playerStats['rbi'] + playerStats['runs'] + playerStats['stolenBases']
    bonusPoints = max(playerStats['hits'] - 3, 0) + max(playerStats['rbi'] - 3, 0) + max(playerStats['runs'] - 3, 0) + max(playerStats['stolenBases'] - 3, 0)
    return points, bonusPoints

def calculateAllBatterPoints(batterPoints, boxscoreData, team):
    for batterId in boxscoreData[team]['batters']:
            playerStats = boxscoreData[team]['players']['ID' + str(batterId)]['stats']['batting']
            points, bonusPoints = calculateBatterPoints(playerStats)
            totalPoints = points + bonusPoints
            if batterId not in batterPoints:
                batterPoints[batterId] = { 
                    'fullName': boxscoreData['playerInfo']['ID' + str(batterId)]['fullName'],
                    'points': 0,
                    'positions': {
                        'C': 0,
                        '1B': 0,
                        '2B': 0,
                        '3B': 0,
                        'SS': 0,
                        'OF': 0,
                        'DH': 0
                    },
                    'eligiblePositions': [],
                    'previousStart': '',
                    'streak': 0
                }
                
            batterInfo = batterPoints[batterId]
            batterInfo['points'] += totalPoints
            if isCurrentYear:
                # If the player's starting position matches their previous starting position, add to the streak
                if batterInfo['previousStart'] == boxscoreData[team]['players']['ID' + str(batterId)]['allPositions'][0]['abbreviation']:
                    batterInfo['streak'] += 1
                    if batterInfo['streak'] == 5 and batterInfo['previousStart'] not in batterInfo['eligiblePositions']:
                        batterInfo['eligiblePositions'].append(batterInfo['previousStart'])
                # Start a new streak
                else:
                    batterInfo['previousStart'] = boxscoreData[team]['players']['ID' + str(batterId)]['allPositions'][0]['abbreviation']
                    batterInfo['streak'] = 1
            # Add a game played to each position, for eligibility tracking
            for position in boxscoreData[team]['players']['ID' + str(batterId)]['allPositions']:
                if position['abbreviation'] in playerPositions:
                    if position['abbreviation'] == 'LF' or position['abbreviation'] == 'CF' or position['abbreviation'] == 'RF':
                        batterInfo['positions']['OF'] += 1
                    else:
                        batterInfo['positions'][position['abbreviation']] += 1
                
def determinePlayerEligibity(batterPoints):
    if isCurrentYear:
        for batterId, batterInfo in batterPoints.items():
            for pos, gamesPlayed in batterInfo['positions'].items():
                if gamesPlayed >= 10 and pos not in batterInfo['eligiblePositions']:
                    batterInfo['eligiblePositions'].append(pos)
    else:
        for batterId, batterInfo in batterPoints.items():
            for pos, gamesPlayed in batterInfo['positions'].items():
                if gamesPlayed >= 20 and pos not in batterInfo['eligiblePositions']:
                    batterInfo['eligiblePositions'].append(pos)
                    
def determinePlayerTeams():
    rosterFile = open('rosters.txt', 'r')
    global playerTeams
    isTeamName = False
    teamName = ''
    for line in rosterFile:
        if line[0] == '~':
            isTeamName = True
            continue
        if isTeamName:
            teamName = line.strip()
            continue
        playerTeams[line.strip().split('-')[0]] = {
            'teamName': teamName,
            'team': line.strip().split('-')[2].split(' ')[0]
        }
    rosterFile.close()

def calculateReliefPitcherPoints(playerStats):
    points = (2 if float(playerStats['inningsPitched']) >= 0.1 else 0) + int(float(playerStats['inningsPitched'])) + 2 * playerStats['wins'] + (3 if 'note' in playerStats and playerStats['note'][1] == 'S' else 0) + playerStats['holds'] - playerStats['earnedRuns'] - playerStats['losses'] - playerStats['blownSaves']
    return points

def calculateAllReliefPitcherPoints(reliefPitcherPoints, boxscoreData, team):
    for pitcherId in boxscoreData[team]['pitchers']:
        if boxscoreData[team]['pitchers'].index(pitcherId) > 0:
            playerStats = boxscoreData[team]['players']['ID' + str(pitcherId)]['stats']['pitching']
            points = calculateReliefPitcherPoints(playerStats)
            if pitcherId not in reliefPitcherPoints:
                reliefPitcherPoints[pitcherId] = { 
                    'fullName': boxscoreData['playerInfo']['ID' + str(pitcherId)]['fullName'],
                    'points': 0,
                    'eligiblePositions': ['RP']
                }
            reliefPitcherPoints[pitcherId]['points'] += points

def calculateStartingPitcherPoints(playerStats):
    points = int(float(playerStats['inningsPitched'])) + (int(float(playerStats['inningsPitched'])) - 5 if(int(float(playerStats['inningsPitched'])) > 5) else 0) + (4 if playerStats['wins'] == 1 else 0) - playerStats['earnedRuns']
    bonusPoints = (2 if (playerStats['runs'] == 0 and float(playerStats['inningsPitched']) >= float(9)) else 0) + (10 if (playerStats['hits'] == 0 and float(playerStats['inningsPitched']) >= float(9)) else 0)
    return points, bonusPoints

def calculateAllStartingPitcherPoints(startingPitcherPoints, boxscoreData, team):
    startingPitcherId = boxscoreData[team]['pitchers'][0]    # Only the starting pitcher of the team
    playerStats = boxscoreData[team]['players']['ID' + str(startingPitcherId)]['stats']['pitching']
    points, bonusPoints = calculateStartingPitcherPoints(playerStats)
    totalPoints = points + bonusPoints
    if startingPitcherId not in startingPitcherPoints:
        startingPitcherPoints[startingPitcherId] = { 
            'fullName': boxscoreData['playerInfo']['ID' + str(startingPitcherId)]['fullName'],
            'points': 0,
            'eligiblePositions': ['SP']
        }
    startingPitcherPoints[startingPitcherId]['points'] += totalPoints
    
def calculatePoints(lineup, reliefPitchers, startingPitchers):  
    sleep(1)
    print('\nBatters:')
    print('{0:<{1}}'.format('Player Name', longestPlayerName), end='|')
    for date in gameDates:
        print(date.split('-', 1)[1], end='|')
    print('Total Points', end='')
    if mode == 'season':
        print('|Weekly Avg', end='')
    print('\n' + '-' * (longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)), end='')
    
    totalBatterPoints = 0
    for playerName in lineup:
        playerID = ''
        playerDailyPoints = []
        if mode == 'weekly':
            playerDailyPoints = ['X'] * len(gameDates)
        totalPlayerPoints = 0
        print('\n{0:<{1}}'.format(playerName, longestPlayerName), end='|')
        for game in games:
            #boxscore_data = statsapi.boxscore_data(game['game_id'])
            boxscore_data = boxscoreDatas[str(game['game_id'])]
            for pID, pInfo in boxscore_data['playerInfo'].items():
                if pInfo['fullName'] == playerName:
                    playerID = pID
                    break
            if playerID == '':
                continue
            playerStats = None
            if int(playerID[2:]) in boxscore_data['away']['batters']:
                playerStats = boxscore_data['away']['players'][playerID]['stats']['batting']
            elif int(playerID[2:]) in boxscore_data['home']['batters']:
                playerStats = boxscore_data['home']['players'][playerID]['stats']['batting']
            if playerStats:
                if mode == 'weekly' and playerDailyPoints[gameDates.index(game['game_date'])] == 'X':
                    playerDailyPoints[gameDates.index(game['game_date'])] = 0
                points, bonusPoints = calculateBatterPoints(playerStats)
                totalPlayerPoints += points + bonusPoints
                if mode == 'weekly':
                    playerDailyPoints[gameDates.index(game['game_date'])] += points + bonusPoints
        for dayPoints in playerDailyPoints:
            print('{0:^5}'.format(dayPoints), end='|')
        totalBatterPoints += totalPlayerPoints
        print('{0:^12}'.format(totalPlayerPoints), end='')
        if mode == 'season':
            print('|{0:^10.2f}'.format(totalPlayerPoints / numWeeks), end='')
        sleep(0.1)
    print('\n{0:<{1}}'.format('TOTAL', longestPlayerName) + ' '*43 + '{0:^12}'.format(totalBatterPoints))

    sleep(1)
    print('\nRelief Pitchers:')
    print('{0:<{1}}'.format('Player Name', longestPlayerName), end='|')
    for date in gameDates:
        print(date.split('-', 1)[1], end='|')
    print('Total Points', end='')
    if mode == 'season':
        print('|Weekly Avg', end='')
    print('\n' + '-' * (longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)), end='')

    totalReliefPitcherPoints = 0
    for playerName in reliefPitchers:
        playerID = ''
        playerDailyPoints = []
        if mode == 'weekly':
            playerDailyPoints = ['X'] * len(gameDates)
        totalPlayerPoints = 0
        print('\n{0:<{1}}'.format(playerName, longestPlayerName), end='|')
        for game in games:
            #boxscore_data = statsapi.boxscore_data(game['game_id'])
            boxscore_data = boxscoreDatas[str(game['game_id'])]
            for pID, pInfo in boxscore_data['playerInfo'].items():
                if pInfo['fullName'] == playerName:
                    playerID = pID
                    break
            if playerID == '':
                continue
            playerStats = None
            if int(playerID[2:]) in boxscore_data['away']['pitchers'] and boxscore_data['away']['pitchers'].index(int(playerID[2:])) != 0:
                playerStats = boxscore_data['away']['players'][playerID]['stats']['pitching']
            elif int(playerID[2:]) in boxscore_data['home']['pitchers'] and boxscore_data['home']['pitchers'].index(int(playerID[2:])) != 0:
                playerStats = boxscore_data['home']['players'][playerID]['stats']['pitching']
            if playerStats:
                if mode == 'weekly' and playerDailyPoints[gameDates.index(game['game_date'])] == 'X':
                    playerDailyPoints[gameDates.index(game['game_date'])] = 0
                points = calculateReliefPitcherPoints(playerStats)
                totalPlayerPoints += points
                if mode == 'weekly':
                    playerDailyPoints[gameDates.index(game['game_date'])] += points
        for dayPoints in playerDailyPoints:
            print('{0:^5}'.format(dayPoints), end="|")
        totalReliefPitcherPoints += totalPlayerPoints
        print('{0:^12}'.format(totalPlayerPoints), end='')
        if mode == 'season':
            print('|{0:^10.2f}'.format(totalPlayerPoints / numWeeks), end='')
        sleep(0.2)
    print('\n{0:<{1}}'.format('TOTAL', longestPlayerName) + ' '*43 + '{0:^12}'.format(totalReliefPitcherPoints))

    sleep(1)
    print('\nStarting Pitchers:')
    print('{0:<{1}}'.format('Player Name', longestPlayerName), end='|')
    for date in gameDates:
        print(date.split('-', 1)[1], end='|')
    print('Total Points', end='')
    if mode == 'season':
        print('|Weekly Avg', end='')
    print('\n' + '-' * (longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)), end='')

    totalStartingPitcherPoints = 0
    numTotalStarts = 0
    for playerName in startingPitchers:
        playerID = ''
        playerDailyPoints = []
        if mode == 'weekly':
            playerDailyPoints = ['X'] * len(gameDates)
        totalPlayerPoints = 0
        print('\n{0:<{1}}'.format(playerName, longestPlayerName), end='|')
        for game in games:
            #boxscore_data = statsapi.boxscore_data(game['game_id'])
            boxscore_data = boxscoreDatas[str(game['game_id'])]
            for pID, pInfo in boxscore_data['playerInfo'].items():
                if pInfo['fullName'] == playerName:
                    playerID = pID
                    break
            if playerID == '':
                continue
            playerStats = None
            if int(playerID[2:]) in boxscore_data['away']['pitchers'] and boxscore_data['away']['pitchers'].index(int(playerID[2:])) == 0:
                playerStats = boxscore_data['away']['players'][playerID]['stats']['pitching']
            elif int(playerID[2:]) in boxscore_data['home']['pitchers'] and boxscore_data['home']['pitchers'].index(int(playerID[2:])) == 0:
                playerStats = boxscore_data['home']['players'][playerID]['stats']['pitching']
            if playerStats:
                points, bonusPoints = calculateStartingPitcherPoints(playerStats)
                if mode == 'weekly':
                    if playerDailyPoints[gameDates.index(game['game_date'])] == 'X':
                        playerDailyPoints[gameDates.index(game['game_date'])] = 0
                    playerDailyPoints[gameDates.index(game['game_date'])] += points + bonusPoints
                numTotalStarts += 1
                if numTotalStarts > 6 and mode == 'weekly':
                    playerDailyPoints[gameDates.index(game['game_date'])] = '(' + str(playerDailyPoints[gameDates.index(game['game_date'])]) + ')'
                    continue
                else:
                    totalPlayerPoints += points + bonusPoints
        for dayPoints in playerDailyPoints:
            print('{0:^5}'.format(dayPoints), end="|")
        totalStartingPitcherPoints += totalPlayerPoints
        print('{0:^12}'.format(totalPlayerPoints), end='')
        if mode == 'season':
            print('|{0:^10.2f}'.format(totalPlayerPoints / numWeeks), end='')
        sleep(0.2)
    if mode == 'weekly':
        print('\n{0:<{1}}'.format('TOTAL', longestPlayerName) + ' '*43 + '{0:^12}'.format(totalStartingPitcherPoints))
        print('\n{0:<{1}}'.format('GRAND TOTAL', longestPlayerName) + ' '*43 + '{0:^12}'.format(totalBatterPoints + totalReliefPitcherPoints + totalStartingPitcherPoints))
        
def writeToCSV(fileName, playerPoints):
    headers = ['Player Name', 'Total Points (' + start_date + '-' + end_date + ')', 'Position']
    with open(fileName, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        # TODO: Find a way to determine what fantasy team a player is on, if any
        for player, info in playerPoints.items():
            csvwriter.writerow([info['fullName'], info['points'], info['eligiblePositions']])
        
# This function calculate points for all players defined by findAllPlayers
# There is no visual output for this function, but exports data as csv
# Also, this will only output player name, total points over the period of time, and position
def calculateAllPlayerPoints():
    outputBattersFileName = 'batterPoints.csv'
    outputReliefPitchersFileName = 'reliefPitchersPoints.csv'
    outputStartingPitchersFileName = 'startingPitchersPoints.csv'
    
    batterPoints = {}
    reliefPitcherPoints = {}
    startingPitcherPoints = {}
    
    print('\nPerforming calculations for all players...')
    # Calculate points, for each game, for each player
    for game in games:
        boxscoreData = boxscoreDatas[str(game['game_id'])]
        # Batter points
        calculateAllBatterPoints(batterPoints, boxscoreData, 'away')
        calculateAllBatterPoints(batterPoints, boxscoreData, 'home')
        # Relief pitcher points
        calculateAllReliefPitcherPoints(reliefPitcherPoints, boxscoreData, 'away')
        calculateAllReliefPitcherPoints(reliefPitcherPoints, boxscoreData, 'home')
        # Starting pitcher points
        calculateAllStartingPitcherPoints(startingPitcherPoints, boxscoreData, 'away')
        calculateAllStartingPitcherPoints(startingPitcherPoints, boxscoreData, 'home')
    print('Calculations complete.')
    
    print('\nDetermining player eligibilities...')
    determinePlayerEligibity(batterPoints)
    print('Eligibilities determined.')
        
    print('\nWriting CSV files...')
    # Write to CSV files
    writeToCSV(outputBattersFileName, batterPoints)
    writeToCSV(outputReliefPitchersFileName, reliefPitcherPoints)
    writeToCSV(outputStartingPitchersFileName, startingPitcherPoints)
    print('Writing complete.')