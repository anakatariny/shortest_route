from rest_framework import serializers
from .models import FileMap, Map


class FileMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMap
        fields = ('id', 'name', 'file')
        read_only = ('id', 'name', 'created_date')
        extra_kwargs = {'file': {'write_only': True}}


class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ('first_edge', 'second_edge', 'value')
