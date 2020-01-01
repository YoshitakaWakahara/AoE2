from django.db import models

class Player(models.Model):
  name = models.CharField(max_length=64)
  rate = models.IntegerField(default=0)
  registered_at = models.DateTimeField('player registeded')

  def __str__(self):
    return self.name

class Team(models.Model):
  team1_total_rate = models.IntegerField(default=0)
  team2_total_rate = models.IntegerField(default=0)
  created_at = models.DateTimeField('team created')
  player = models.ForeignKey(Player, on_delete=models.CASCADE)