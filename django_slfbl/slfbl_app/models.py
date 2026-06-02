from django.db import models

from slfbl_app.static_functions import normalizeName
    
class SlfblTeam(models.Model):
    name = models.CharField(max_length=100)
    name_normalized = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name_normalized = normalizeName(self.name)
        super().save(*args, **kwargs)
    
class Player(models.Model):
    playerId = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    name_normalized = models.CharField(max_length=100)
    qualifiedPositions = models.CharField(max_length=100)
    positionsPlayed = models.JSONField(default=dict)
    mlbTeam = models.CharField(max_length=10)
    slfblTeam = models.ForeignKey(SlfblTeam, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name_normalized = normalizeName(self.name)
        super().save(*args, **kwargs)
    
class DailyPlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateField()
    points = models.IntegerField()
    gameId = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.player.name} - {self.date}"
    
class DailyPlayerStatForDates(models.Model):
    playerId = models.IntegerField()
    name = models.CharField(max_length=100)
    points = models.CharField(max_length=100)  # This will store the array of points as a string
    totalPoints = models.IntegerField()
    qualifiedPositions = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} - {self.totalPoints}"
    
class WeeklyPlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField()
    weekStartDate = models.DateField()
    weekEndDate = models.DateField()
    def __str__(self):
        return f"{self.player.name} - Week ({self.weekStartDate} to {self.weekEndDate})"
    
class SeasonPlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    points = models.IntegerField()
    seasonYear = models.IntegerField()
    def __str__(self):
        return f"{self.player.name} - Season {self.seasonYear}"