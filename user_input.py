### Start user-defined variables

#lineup = []
#startingPitchers = []

lineup = ['Aaron Judge', 'J.T. Realmuto', 'Yandy Díaz', 'Marcus Semien', 'Rafael Devers', 'Bo Bichette', 'Teoscar Hernández', 'Anthony Santander', 'Brandon Nimmo']
reliefPitchers = ['David Robertson', 'Héctor Neris', 'A.J. Minter']
startingPitchers = ['Jordan Montgomery', 'Dylan Cease', 'Sonny Gray', 'Mitch Keller', 'Charlie Morton']

#bench_lineup = []
#bench_reliefPitchers = []
#bench_startingPitchers = []
bench_lineup = ['Thairo Estrada', 'Eugenio Suarez', 'Isaac Paredes', 'Justin Turner', 'Luis Arraez']
bench_reliefPitchers = ['Bryan Abreu']
bench_startingPitchers = ['Blake Snell', 'Kyle Gibson']

#DV_lineup = []
#DV_reliefPitchers = []
#DV_startingPitchers = []
DV_lineup = ['Edmundo Sosa', 'Luis García Jr.', 'Drew Waters', 'Edwin Arroyo', 'Alec Burleson', 'Michael Busch', 'Endy Rodríguez', 'Juan Yepez']
DV_reliefPitchers = ['Nick Lodolo', 'Aaron Ashby', 'Wilmer Flores', 'Gordon Graceffo', 'Quinn Priester', 'Paul Skenes', 'Owen White']
DV_startingPitchers = ['Nick Lodolo', 'Aaron Ashby', 'Wilmer Flores', 'Gordon Graceffo', 'Quinn Priester', 'Paul Skenes', 'Owen White']

opp_lineup = ['Jonah Heim', 'Matt Olson', 'Ryan McMahon', 'Elly De La Cruz', 'Carlos Correa', 'Yordan Alvarez', 'Seiya Suzuki', 'Tyler O\'Neill', 'Willy Adames']
opp_reliefPitchers = ['David Bednar', 'Jordan Leasure', 'Griffin Jax']
opp_startingPitchers = ['Jared Jones', 'Pablo Lopez', 'Christian Scott', 'Kevin Gausman']

start_date = '05/20/2024'   # Beginning of season = 04/07/2022, 03/30/2023
end_date = '05/26/2024'     # End of season = 10/05/2022, 10/02/2023
mode = 'weekly'             # Either season or weekly
doDownloadScores = True    # Flag to tell whether to download from API or read from file
doAllPlayers = False         # Flag to tell whether to run for listed players or all players
isCurrentYear = True         # Flag to tell whether the start and end date are for the current year or not

### End user-defined variables