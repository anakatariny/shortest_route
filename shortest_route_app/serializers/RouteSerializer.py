from rest_framework import serializers
from shortest_route_app.models import Route


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ('file_id', 'origin', 'destination', 'minimum_route', 'distance')
