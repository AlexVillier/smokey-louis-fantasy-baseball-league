from datetime import date, timedelta
from django.core.management.base import BaseCommand
from slfbl_app.db_functions import calculateAllBatterPoints, calculateAllReliefPitcherPoints, calculateAllStartingPitcherPoints
from slfbl_app.api_calls import getGames, getBoxscoreData

class Command(BaseCommand):
    help = "Fetch and persist daily player stats"

    def handle(self, *args, **options):
        start_date = "03/25/2026"       # MLB season started March 25th
        end_date = "05/27/2026"
        current_date = start_date
        while current_date <= end_date:
            #current_date = date.today().strftime("%m/%d/%Y")
            #current_date = "05/04/2026"
            self.stdout.write(f"Finding and persisting daily player stats for {current_date}...")
            games = getGames(current_date, current_date)
            for game in games:
                self.stdout.write(f"Game {game['game_id']}")
                boxscoreData = getBoxscoreData(game['game_id'])
                calculateAllBatterPoints(boxscoreData, True)
                calculateAllReliefPitcherPoints(boxscoreData)
                calculateAllStartingPitcherPoints(boxscoreData)
            self.stdout.write("Finished updating daily player stats.")
            # Increment the date by one day
            current_date = (date.strptime(current_date, "%m/%d/%Y") + timedelta(days=1)).strftime("%m/%d/%Y")