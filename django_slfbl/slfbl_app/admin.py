from django.contrib import admin
from .models import SlfblTeam, Player, DailyPlayerStats, WeeklyPlayerStats, SeasonPlayerStats

# Register your models here.
class SlfblTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "qualifiedPositions", "mlbTeam", "slfblTeam")
    search_fields = ["name_normalized"]

class DailyPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ("player", "player__qualifiedPositions", "date", "points", "gameId")
    search_fields = ["player__name_normalized", "player__qualifiedPositions"]

class WeeklyPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ("player", "points", "weekStartDate", "weekEndDate")

class SeasonPlayerStatsAdmin(admin.ModelAdmin):
    list_display = ("player", "points", "seasonYear")

admin.site.register(SlfblTeam, SlfblTeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(DailyPlayerStats, DailyPlayerStatsAdmin)
admin.site.register(WeeklyPlayerStats, WeeklyPlayerStatsAdmin)
admin.site.register(SeasonPlayerStats, SeasonPlayerStatsAdmin)