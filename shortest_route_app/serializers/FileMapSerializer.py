from rest_framework import serializers
from shortest_route_app.models import FileMap


class FileMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMap
        fields = ('id', 'name', 'file')
        read_only = ('id', 'name', 'created_date')
        extra_kwargs = {'file': {'write_only': True}}
