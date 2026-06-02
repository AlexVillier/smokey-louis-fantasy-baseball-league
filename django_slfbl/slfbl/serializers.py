from django.contrib.auth.models import Group, User
from rest_framework import serializers

from slfbl_app.models import DailyPlayerStatForDates, DailyPlayerStats, Player, SeasonPlayerStats, SlfblTeam, WeeklyPlayerStats


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
        
class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ["url", "playerId", "name", "qualifiedPositions", "mlbTeam", "slfblTeam"]

class DailyPlayerStatsSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField()
    class Meta:
        model = DailyPlayerStatForDates
        fields = ["id", "player", "playerId", "name", "points", "totalPoints", "qualifiedPositions"]

class WeeklyPlayerStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WeeklyPlayerStats
        fields = ["url", "player", "points", "weekStartDate", "weekEndDate"]

class SeasonPlayerStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SeasonPlayerStats
        fields = ["url", "player", "points", "seasonYear"]

class SlfblTeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SlfblTeam
        fields = ["url", "id", "name", "owner"]