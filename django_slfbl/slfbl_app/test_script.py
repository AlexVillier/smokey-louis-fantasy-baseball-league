import statsapi

print('Running test script...\n')

#res = statsapi.schedule(start_date='08/01/2025', end_date='08/01/2025')
res = statsapi.boxscore_data('823384')
print('API call result:')
print(res)

print('Test script complete.')