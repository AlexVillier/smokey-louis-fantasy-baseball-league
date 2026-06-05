from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django_slfbl.slfbl_app.models import DailyPlayerStats
from slfbl_app.db_functions import calculateAllBatterPoints, calculateAllReliefPitcherPoints, calculateAllStartingPitcherPoints
from slfbl_app.api_calls import getGames, getBoxscoreData

class Command(BaseCommand):
    help = "Fetch and persist daily player stats"

    def handle(self, *args, **options):

        # Delete all existing daily stats before recalculating them to ensure that the stats are accurate and up-to-date.
        DailyPlayerStats.objects.all().delete()

        # Calculate stats for all games from the start of the season to today (exclusive)
        start_date = "03/25/2026"       # MLB season started March 25th, 2026
        end_date = (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")  # Exclude today's games since they may not be finished yet
        games = getGames(start_date, end_date)
        for game in games:
            boxscoreData = getBoxscoreData(game['game_id'])
            calculateAllBatterPoints(boxscoreData, True)
            calculateAllReliefPitcherPoints(boxscoreData)
            calculateAllStartingPitcherPoints(boxscoreData)