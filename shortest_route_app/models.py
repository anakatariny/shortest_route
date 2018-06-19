from django.db import models
from django.utils import timezone

#this class take care of the file information and validates the format
class FileMap(models.Model):
    name = models.CharField(max_length=300, unique=True, blank=False)
    file = models.FileField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement openFile
    #TODO validate file
    #TODO save file

    def __str__(self):
        return self.name

#this class take care of the map information inside the file
class Map(models.Model):
    file_id = models.ForeignKey('shortest_route_app.FileMap', on_delete=models.CASCADE)
    first_edge = models.CharField(max_length=200, blank=False)
    second_edge = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement saveMap
    #TODO implement calculate route

    def __str__(self):
        return [self.first_edge, self.second_edge, self.value]

#this class have all the calculated routes
class Route(models.Model):
    file_id = models.ForeignKey('shortest_route_app.FileMap', on_delete=models.CASCADE)
    origin = models.CharField(max_length=200, blank=False)
    destiny = models.CharField(max_length=200, blank=False)
    distance = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)


    #TODO implement getRoute

    def __str__(self):
        return [self.origin, self.destiny, self.distance]