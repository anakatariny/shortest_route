from rest_framework import serializers
from .models import FileMap


class FileMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMap
        fields = ('id','name', 'file')
        read_only = ('id','name', 'file', 'created_date')