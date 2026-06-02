from datetime import date, datetime

from slfbl_app.api_calls import getGames
from slfbl_app.functions import calculateBatterPoints, calculateReliefPitcherPoints, calculateStartingPitcherPoints
from slfbl_app.models import DailyPlayerStats, Player

def findAndPersistDailyPlayerStats():
    currentDate = date.today().strftime("%m/%d/%Y")
    print(f"Finding and persisting daily player stats for {currentDate}...")
    games = getGames(currentDate, currentDate)
    for game in games:
        print(f"Game {game['game_id']}")

playerPositions = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF']

def calculateAllBatterPoints(boxscoreData, isCurrentYear):
    for team in ['home', 'away']:
        if boxscoreData[team]['batters'] is None or len(boxscoreData[team]['batters']) == 0:
            continue
        for batterId in boxscoreData[team]['batters']:
                playerStats = boxscoreData[team]['players']['ID' + str(batterId)]['stats']['batting']
                points, bonusPoints = calculateBatterPoints(playerStats)
                totalPoints = points + bonusPoints
                batterInfo = { 
                    'fullName': boxscoreData['playerInfo']['ID' + str(batterId)]['fullName'],
                    'points': 0,
                    'positions': {
                        'C': 0,
                        '1B': 0,
                        '2B': 0,
                        '3B': 0,
                        'SS': 0,
                        'OF': 0,
                        'DH': 0,
                        'streak': {
                            'position': '',
                            'count': 0
                        }
                    },
                    'eligiblePositions': [],
                    'previousStart': '',
                    'streak': 0
                }
                    
                batterInfo['points'] += totalPoints
                if isCurrentYear:
                    # If the player's starting position matches their previous starting position, add to the streak
                    if batterInfo['previousStart'] == boxscoreData[team]['players']['ID' + str(batterId)]['allPositions'][0]['abbreviation']:
                        batterInfo['streak'] += 1
                        if batterInfo['streak'] == 5 and batterInfo['previousStart'] not in batterInfo['eligiblePositions']:
                            batterInfo['eligiblePositions'].append(batterInfo['previousStart'])
                    # Start a new streak
                    else:
                        positionPlayed = boxscoreData[team]['players']['ID' + str(batterId)]['allPositions'][0]['abbreviation']
                        if positionPlayed in playerPositions:
                            batterInfo['previousStart'] = positionPlayed
                            batterInfo['streak'] = 1
                # Add a game played to each position, for eligibility tracking
                for position in boxscoreData[team]['players']['ID' + str(batterId)]['allPositions']:
                    if position['abbreviation'] in playerPositions:
                        if position['abbreviation'] == 'LF' or position['abbreviation'] == 'CF' or position['abbreviation'] == 'RF':
                            batterInfo['positions']['OF'] += 1
                            batterInfo['previousStart'] = 'OF'
                        else:
                            batterInfo['positions'][position['abbreviation']] += 1

                player = Player.objects.filter(playerId=batterId).first()
                if player is None:
                    print(f"Player {batterInfo['fullName']} not found in database, creating new player...")
                    player = Player.objects.create(
                        playerId=batterId,
                        name=batterInfo['fullName'],
                        mlbTeam=boxscoreData['teamInfo'][team]['abbreviation'],
                        positionsPlayed=batterInfo['positions']
                    )
                else:
                    # Update the player's positions played for the season
                    position = batterInfo['previousStart']
                    if position != '':
                        player.positionsPlayed[position] = int(player.positionsPlayed[position]) + int(batterInfo['positions'][position])
                        if player.positionsPlayed['streak']['position'] != position:
                            player.positionsPlayed['streak']['position'] = position
                            player.positionsPlayed['streak']['count'] = 1
                        else:
                            player.positionsPlayed['streak']['count'] += 1
                            if player.positionsPlayed['streak']['count'] == 5 and player.positionsPlayed['streak']['position'] not in player.qualifiedPositions:
                                if player.qualifiedPositions != '':
                                    player.qualifiedPositions += '/'
                                player.qualifiedPositions += player.positionsPlayed['streak']['position']
                            if isCurrentYear:
                                for pos, gamesPlayed in player.positionsPlayed.items():
                                    if pos != 'streak' and gamesPlayed >= 10 and pos not in batterInfo['eligiblePositions']:
                                        batterInfo['eligiblePositions'].append(pos)
                            else:
                                for pos, gamesPlayed in player.positionsPlayed.items():
                                    if pos != 'streak' and gamesPlayed >= 20 and pos not in batterInfo['eligiblePositions']:
                                        batterInfo['eligiblePositions'].append(pos)
                        player.save()

                if not DailyPlayerStats.objects.filter(player=player, gameId=boxscoreData['gameId']).exists():
                    DailyPlayerStats.objects.create(
                        player=player,
                        date=datetime.strptime(boxscoreData['gameBoxInfo'][len(boxscoreData['gameBoxInfo']) - 1]['label'], "%B %d, %Y").date(), # Last index is the date in the gameBoxInfo list
                        points=batterInfo['points'],
                        gameId=boxscoreData['gameId']
                    )

def calculateAllReliefPitcherPoints(boxscoreData):
    for team in ['home', 'away']:
        if boxscoreData[team]['pitchers'] is None or len(boxscoreData[team]['pitchers']) <= 1:   # If there are no pitchers or only a starting pitcher, skip
            continue
        for pitcherId in boxscoreData[team]['pitchers']:
            if boxscoreData[team]['pitchers'].index(pitcherId) > 0:
                playerStats = boxscoreData[team]['players']['ID' + str(pitcherId)]['stats']['pitching']
                points = calculateReliefPitcherPoints(playerStats)
                playerName = boxscoreData['playerInfo']['ID' + str(pitcherId)]['fullName']

                player = Player.objects.filter(playerId=pitcherId).first()
                if player is None:
                    print(f"Player {playerName} not found in database, creating new player...")
                    player = Player.objects.create(
                        playerId=pitcherId,
                        name=playerName,
                        mlbTeam=boxscoreData['teamInfo'][team]['abbreviation']
                    )
                
                if 'RP' not in player.qualifiedPositions:
                    if player.qualifiedPositions != '':
                        player.qualifiedPositions += '/'
                    player.qualifiedPositions += 'RP'
                    player.save()

                dailyPlayerStatsForPlayer = DailyPlayerStats.objects.filter(player=player, gameId=boxscoreData['gameId']).first()
                if dailyPlayerStatsForPlayer is None:
                    DailyPlayerStats.objects.create(
                        player=player,
                        date=datetime.strptime(boxscoreData['gameBoxInfo'][len(boxscoreData['gameBoxInfo']) - 1]['label'], "%B %d, %Y").date(), # Last index is the date in the gameBoxInfo list
                        points=points,
                        gameId=boxscoreData['gameId']
                    )
                else:
                    dailyPlayerStatsForPlayer.points += points
                    dailyPlayerStatsForPlayer.save()

def calculateAllStartingPitcherPoints(boxscoreData):
    for team in ['home', 'away']:
        if boxscoreData[team]['pitchers'] is None or len(boxscoreData[team]['pitchers']) == 0:
            continue
        startingPitcherId = boxscoreData[team]['pitchers'][0]    # Only the starting pitcher of the team
        playerStats = boxscoreData[team]['players']['ID' + str(startingPitcherId)]['stats']['pitching']
        totalPoints = calculateStartingPitcherPoints(playerStats)

        playerName = boxscoreData['playerInfo']['ID' + str(startingPitcherId)]['fullName']
        player = Player.objects.filter(playerId=startingPitcherId).first()
        if player is None:
            print(f"Player {playerName} not found in database, creating new player...")
            player = Player.objects.create(
                playerId=startingPitcherId,
                name=playerName,
                mlbTeam=boxscoreData['teamInfo'][team]['abbreviation']
            )
        
        if 'SP' not in player.qualifiedPositions:
            if player.qualifiedPositions != '':
                player.qualifiedPositions += '/'
            player.qualifiedPositions += 'SP'
            player.save()

        dailyPlayerStatsForPlayer = DailyPlayerStats.objects.filter(player=player, gameId=boxscoreData['gameId']).first()
        if dailyPlayerStatsForPlayer is None:
            DailyPlayerStats.objects.create(
                player=player,
                date=datetime.strptime(boxscoreData['gameBoxInfo'][len(boxscoreData['gameBoxInfo']) - 1]['label'], "%B %d, %Y").date(), # Last index is the date in the gameBoxInfo list
                points=totalPoints,
                gameId=boxscoreData['gameId']
            )
        else:
            dailyPlayerStatsForPlayer.points += totalPoints
            dailyPlayerStatsForPlayer.save()

def updateSlfblRosters():
    print("Updating SLFBL rosters...")
    pass