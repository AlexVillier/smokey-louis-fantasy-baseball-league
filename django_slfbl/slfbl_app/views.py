from datetime import datetime

from django.shortcuts import render

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from django.db import connection, models
from slfbl.serializers import DailyPlayerStatsSerializer, PlayerSerializer, SeasonPlayerStatsSerializer, SlfblTeamSerializer, WeeklyPlayerStatsSerializer
from slfbl_app.models import DailyPlayerStatForDates, DailyPlayerStats, Player, SeasonPlayerStats, SlfblTeam, WeeklyPlayerStats

# Create your views here.
class PlayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows players to be viewed.
    """

    queryset = Player.objects.all().order_by("name")
    serializer_class = PlayerSerializer

class TempDate(models.Model):
    date = models.DateField()

    class Meta:
        managed = False  # This model won't create a table in the database
        db_table = 'temp_dates'  # Name of the temporary table

class DailyPlayerStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows daily player stats to be viewed.
    """

    queryset = DailyPlayerStats.objects.none()  # Required for DRF router
    serializer_class = DailyPlayerStatsSerializer

    def _normalize_date(self, value):
        for fmt in ("%Y/%m/%d", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt).date().isoformat()
            except (TypeError, ValueError):
                continue
        raise ValueError("Invalid date format")

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        player_id = request.query_params.get("player_id")
        team_id = request.query_params.get("slfbl_team_id")

        if not start_date or not end_date:
            return Response(
                {"detail": "start_date and end_date query params are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if player_id and team_id:
            player_id = None    # Give team_id precedence

        try:
            start_date = self._normalize_date(start_date)
            end_date = self._normalize_date(end_date)
        except ValueError:
            return Response(
                {"detail": "Dates must be in YYYY/MM/DD or YYYY-MM-DD format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sql = f"""
            WITH RECURSIVE date_series AS (
                SELECT '{start_date}' as date
                UNION ALL
                SELECT date(date, '+1 day')
                FROM date_series
                WHERE date < '{end_date}'
            )
            SELECT
                p.id AS player_id,
                p.name,
                GROUP_CONCAT(COALESCE(dps.points, 'X'), ',') AS points,
                SUM(COALESCE(dps.points, 0)) AS totalPoints,
                p.qualifiedPositions
            FROM slfbl_app_player p
            CROSS JOIN date_series ds
            LEFT JOIN slfbl_app_dailyplayerstats dps
                ON dps.player_id = p.id AND dps.date = ds.date
            {f" WHERE p.id = {player_id}" if player_id else ""}
            {f" WHERE p.slfblTeam_id = {team_id}" if team_id else ""}
            GROUP BY p.id, p.name
            ORDER BY p.name
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        results = []
        for player_id, name, points, total_points, qualified_positions in rows:
            results.append(
                {
                    "playerId": player_id,
                    "name": name,
                    "points": points.split(",") if points else [],
                    "totalPoints": total_points or 0,
                    "qualifiedPositions": qualified_positions if qualified_positions else ""
                }
            )

        return Response(results)

class WeeklyPlayerStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows weekly player stats to be viewed.
    """

    queryset = WeeklyPlayerStats.objects.all().order_by("weekStartDate")
    serializer_class = WeeklyPlayerStatsSerializer

class SeasonPlayerStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows season player stats to be viewed.
    """

    queryset = SeasonPlayerStats.objects.all().order_by("seasonYear")
    serializer_class = SeasonPlayerStatsSerializer

class SlfblTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows SLFBL teams to be viewed.
    """

    queryset = SlfblTeam.objects.all().order_by("name")
    serializer_class = SlfblTeamSerializer