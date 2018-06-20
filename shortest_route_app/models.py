from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def is_number(possible_value):
    """
    this functions checks if the third value from a row is a number or can be converted in one
    :param possible_value: the value that will be tested, the validation is correct if the value is a float
    :return: boolean
    """
    try:
        float(possible_value)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(possible_value)
        return True
    except (TypeError, ValueError):
        pass
    return False



def validate_file(self):
    """
    this functions checks if the file uploaded is in the expected format
    :param self: fileMap
    :return: fileMap
    """
    try:
        fileMap = self.readlines()
    except:
        raise ValidationError(
            "Invalid File. Can't open file.")
    line_number = 1
    for line in fileMap:
        # Separate content by space, dividing each line into 3 columns to evaluate the contents of the file
        strLine = line.decode("utf-8")
        splited_line = strLine.split(" ")
        # if the file don't have 3 columns each line, or the third value is not a number throw the error
        if (len(splited_line) != 3):
            raise ValidationError(
                "Invalid File. Error in line " + str(line_number) + ". Format invalid.")
        if not is_number(splited_line[2]):
            raise ValidationError("Invalid File. Error in line " + str(line_number) + ". Invalid value.")
        line_number += 1

    return self


class FileMap(models.Model):
    """
    this class take care of the file information
    """
    name = models.CharField(max_length=300, unique=True, blank=False)
    file = models.FileField(blank=False, null=False, upload_to='maps/', validators=[validate_file])
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

@receiver(post_save, sender=FileMap)
def save_points(sender, instance, **kwargs):
    """
    :param sender:
    :param instance: File with the map
    :param kwargs:
    :return: points saved
    """
    print('post save callback' + str(instance.id))
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
        point = Map(file_id=instance,
                    first_edge=splited_line[0],
                    second_edge=splited_line[1],
                    value=float(splited_line[2]))
        try:
            point.save()
        except (TypeError, ValueError):
            instance.delete()
            raise ValidationError(
                "Invalid File. Can't save the map.")
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

    #TODO implement saveMap
    #TODO implement calculate route

    def __str__(self):
        return "first_edge:" + self.first_edge + "; second_edge:" + self.second_edge + "; value:" + str(self.value)


class Route(models.Model):
    """
    this class have all the calculated routes
    """
    file_id = models.ForeignKey('shortest_route_app.FileMap', on_delete=models.CASCADE)
    origin = models.CharField(max_length=200, blank=False)
    destiny = models.CharField(max_length=200, blank=False)
    minimum_route = models.CharField(max_length=400, blank=False)
    distance = models.FloatField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now)

    #TODO implement getRoute

    def __str__(self):
        return [self.origin, self.destiny, self.distance]