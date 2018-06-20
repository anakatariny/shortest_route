import hashlib
import hmac
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from shortest_route.settings import SECRET_KEY
from shortest_route_app.models import Map


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
        file_map = self.readlines()
    except (TypeError, ValueError):
        raise ValidationError(
            "Invalid File. Can't open file.")
    line_number = 1
    for line in file_map:
        # Separate content by space, dividing each line into 3 columns to evaluate the contents of the file
        str_line = line.decode("utf-8")
        splited_line = str_line.split(" ")
        # if the file don't have 3 columns each line, or the third value is not a number throw the error
        if len(splited_line) != 3:
            raise ValidationError(
                "Invalid File. Error in line " + str(line_number) + ". Format invalid.")
        if not is_number(splited_line[2]):
            raise ValidationError("Invalid File. Error in line " + str(line_number) + ". Invalid value.")
        line_number += 1
    key = bytes(SECRET_KEY, 'UTF-8')
    new_file_name = hmac.new(key, self.name.encode('utf-8'), hashlib.sha256).hexdigest()
    self.name = new_file_name + ".txt"

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


