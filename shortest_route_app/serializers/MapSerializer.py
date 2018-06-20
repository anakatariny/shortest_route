from rest_framework import serializers
from shortest_route_app.models import Map


class MapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ('first_edge', 'second_edge', 'value')
