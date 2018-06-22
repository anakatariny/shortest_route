from django.db import models
from django.utils import timezone


class Route(models.Model):
    """
    this class have all the calculated routes
    """
    file_id = models.ForeignKey('FileMap', on_delete=models.CASCADE)
    origin = models.CharField(max_length=200, blank=False)
    destination = models.CharField(max_length=200, blank=False)
    minimum_route = models.CharField(max_length=400, blank=False)
    distance = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement getRoute

    def __str__(self):
        return "map_id:" + self.file_id.name + "; origin:" + self.origin + "; destination:" + self.destination + \
               "; path:" + self.minimum_route + "; distance:" + str(self.distance)