from fantasy_points_new import *

########################
### MAIN ENTRY POINT ###
###  RUN THIS FILE   ###
########################

print('Calculating...\n')

findDatesAndBoxscores()

if doAllPlayers:
    calculateAllPlayerPoints()
else:
    determineLongestPlayerName([lineup, reliefPitchers, startingPitchers, bench_lineup, bench_reliefPitchers, bench_startingPitchers, DV_lineup, DV_reliefPitchers, DV_startingPitchers, opp_lineup, opp_reliefPitchers, opp_startingPitchers])              
    print('STARTERS')
    calculatePoints(lineup, reliefPitchers, startingPitchers)
    print('\n' + '='*(longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)))

    print('BENCH')
    calculatePoints(bench_lineup, bench_reliefPitchers, bench_startingPitchers)
    print('\n' + '='*(longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)))

    print('DV SQUAD')
    calculatePoints(DV_lineup, DV_reliefPitchers, DV_startingPitchers)
    print('\n' + '='*(longestPlayerName + 1 + len(gameDates) * 6 + 12 + (11 if mode == 'season' else 0)))

    print('OPPONENT')
    calculatePoints(opp_lineup, opp_reliefPitchers, opp_startingPitchers)

print('\nFinished.')