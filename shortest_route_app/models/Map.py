from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def save_points_from_file(instance):
    """
    :param sender:
    :param instance: File with the map
    :param kwargs:
    :return: points saved
    """
    try:
        file_map = instance.file.readlines()
    except (TypeError, ValueError):
        raise ValidationError(
            "Invalid File. Can't open file.")
    line_number = 1
    for line in file_map:
        # Separate content by space, dividing each line into 3 columns to evaluate the contents of the file
        str_line = line.decode("utf-8")
        splited_line = str_line.split(" ")
        point = Map.objects.filter(file_id=instance, first_edge=splited_line[0], second_edge=splited_line[1]).first()
        if point is not None:
            point.value = float(splited_line[2])
        else:
            point = Map(file_id=instance,
                        first_edge=splited_line[0],
                        second_edge=splited_line[1],
                        value=float(splited_line[2]))
        try:
            point.save()
        except (TypeError, ValueError):
            raise ValidationError(
                "Invalid File. Can't save the map.")
        line_number += 1


def save_points_from_json(file_map,json):
    """
    :param sender:
    :param instance: File with the map
    :param kwargs:
    :return: points saved
    """
    line_number = 1
    # check if json has content
    if len(json) == 0:
        raise ValidationError('Empty JSON.')
    for line in json:
        try:
            point = Map.objects.filter(file_id=file_map, first_edge=line['first_edge'], second_edge=line['second_edge']).first()
            if point is not None:
                point.value = float(line['value'])
            else:
                point = Map(file_id=file_map,
                            first_edge=line['first_edge'],
                            second_edge=line['second_edge'],
                            value=float(line['value']))
                point.save()
        except (TypeError, ValueError):
            raise ValidationError(
                "Invalid json. Can't save the map.")
        line_number += 1


class Map(models.Model):
    """
    this class take care of the map information inside the file
    """
    file_id = models.ForeignKey('shortest_route_app.FileMap', on_delete=models.CASCADE)
    first_edge = models.CharField(max_length=200, blank=False)
    second_edge = models.CharField(max_length=200, blank=False)
    value = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    """
    overrides the django function to put the capitalized name in the bank
    """
    def save(self, *args, **kwargs):
        self.first_edge = self.first_edge.upper()
        self.second_edge = self.second_edge.upper()
        super(Map, self).save(*args, **kwargs)

    def get_edge(self):
        """
        :return: returns the information in a vector so the graph can use it
        """
        return (self.first_edge, self.second_edge, self.value)

    def __str__(self):
        return "first_edge:" + self.first_edge + "; second_edge:" + self.second_edge + "; value:" + str(self.value)

