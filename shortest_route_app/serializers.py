from rest_framework import serializers
from .models import FileMap

class FileMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMap
        fields = ('name', 'file')
        read_only = ('name', 'file', 'created_date')
