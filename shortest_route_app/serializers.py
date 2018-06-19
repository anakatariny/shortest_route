from rest_framework import serializers
from .models import FileMap

# this functions checks if the third value from a row is a number or can be converted in one
def is_number(possible_value):
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

class FileMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMap
        fields = ('name', 'file')
        file = serializers.FileField()
        read_only = ('name', 'file', 'created_date')

        # this function open the file and read all the content, looking for format errors checked by is_number
        def validate_file(self, file):
            try:
                file_open = open(file, "r")
            except ValueError:
                raise serializers.ValidationError("Can't open file.")
            # reading each line into a list
            fl = file_open.readlines()
            line_number = 1
            for line in fl:
                # Separate content by space, dividing each line into 3 columns to evaluate the contents of the file
                splited_line = line.split(" ")
                # if the file don't have 3 columns each line, or the third value is not a number throw the error
                if (len(splited_line) != 3):
                    raise serializers.ValidationError(
                        "Invalid File. Error in line " + line_number + ". Format invalid.")
                if not is_number(splited_line[2]):
                    raise serializers.ValidationError("Invalid File. Error in line " + line_number + ". Invalid value.")
                line_number += 1
            return file
