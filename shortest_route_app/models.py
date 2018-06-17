from django.db import models
from django.utils import timezone

class Map(models.Model):
    name = models.CharField(max_length=300)
    path = models.CharField(max_length=300)
    created_date = models.DateTimeField(
            default=timezone.now)

    def uploadMap(self):
        #TODO implement this method

    def __str__(self):
        return self.name


class Route(models.Model):
    map_id = models.ForeignKey('models.Map', on_delete=models.CASCADE)
    origin = models.CharField(max_length=200)
    destiny = models.CharField(max_length=200)
    distance = models.FloatField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def getRoute(self):
        #TODO implement this method

    def __str__(self):
        return self.origin, self.destiny