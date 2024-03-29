from django.db import models

# Create your models here.


class Team(models.Model):
    teamId = models.CharField(max_length=20)
    route = models.CharField(max_length=200, blank=True)
    index = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.teamId
