from django.db import models
from django.utils import timezone

#this class take care of the map information through the file
class Map(models.Model):
    name = models.CharField(max_length=300, unique=True)
    path = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement openMap
    #TODO implement saveMap
    #TODO implement Djistra
    #TODO implement uploadMap

    def __str__(self):
        return self.name

#this class take care of all the routes informations in each map
class Route(models.Model):
    map_id = models.ForeignKey('shortest_route_app.Map', on_delete=models.CASCADE)
    origin = models.CharField(max_length=200)
    destiny = models.CharField(max_length=200)
    distance = models.FloatField()
    created_date = models.DateTimeField(default=timezone.now)


    #TODO implement getRoute

    def __str__(self):
        return [self.origin, self.destiny, self.distance]