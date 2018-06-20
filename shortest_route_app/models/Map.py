from django.db import models
from django.utils import timezone


class Map(models.Model):
    """
    this class take care of the map information inside the file
    """
    file_id = models.ForeignKey('shortest_route_app.FileMap', on_delete=models.CASCADE)
    first_edge = models.CharField(max_length=200, blank=False)
    second_edge = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement saveMap
    #TODO implement calculate route

    def __str__(self):
        return "first_edge:" + self.first_edge + "; second_edge:" + self.second_edge + "; value:" + str(self.value)

