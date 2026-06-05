# Versioning File for Smokey Louis Fantasy Baseball League Points Project

## Version History

### v0.3.8
* Updated `update_daily_stats` to only run for the previous day's games
* Added `refresh_daily_stats` command, which purges all daily stats and then recalculates all stats until the previous day

### v0.3.7
* Added scheduler to run `update_daily_stats` once a day at 5am
* Added scheduler to run `update_weekly_stats` once a week on Mondays at 5am

### v0.3.6
* Added Start Date and End Date fields to the Matchup page

### v0.3.5
* Updated to still support development mode
* Fixes too many re-renders error on Matchup page

### v0.3.4
* Created docker-compose to run backend and frontend in separate containers

### v0.3.3
* Made debug_toolbar import conditional to dev mode and not in production mode

### v0.3.2
* Added production settings files for production environment

### v0.3.1
* Added Dockerfile and requirements.txt for production container environment

### v0.3.0
* Added Django database/backend
* Created the Points, Player, and Matchup pages
* Created scripts for maintaining database objects

### v0.2.0
* Created React (Vite) front-end app

### v0.1.0
* Split out api calls into `api_calls.py` for better maintainability, and added documentation

### v0.0.1
* Initial commits and files