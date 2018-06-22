from rest_framework.views import APIView
from rest_framework.response import Response
from shortest_route_app.serializers import MapSerializer
from shortest_route_app.models import Map


class MapView(APIView):
    """
    get each row in the database
    """
    serializer_class = MapSerializer
    queryset = Map.objects.all()

    def get(self, request, format=None):
        points_list = Map.objects.all()
        # get all the map fields
        result = []
        for point in points_list:
            result.append("map_id:"+point.file_id.name+"; first_edge:"+point.first_edge+"; second_edge:"+point.second_edge+"; value:"+str(point.value))

        return Response({'maps': result})

