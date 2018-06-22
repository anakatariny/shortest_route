from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from shortest_route_app.models import FileMap
from shortest_route_app.models.Map import save_points_from_file, save_points_from_json
from shortest_route_app.serializers.FileMapSerializer import FileMapSerializer


class FileMapView(APIView):
    """
    This class contain API handlers to manipulate the file map with methods GET, POST and DELETE
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = FileMapSerializer
    queryset = FileMap.objects.all()

    def get(self, request, format=None):
        maps_list = FileMap.objects.all()
        result = []
        for map in maps_list:
            result.append("id:"+str(map.id)+"; nome:"+map.name)

        return Response({'maps': result}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        file_serializer = FileMapSerializer(data=request.data)
        try:
            with transaction.atomic():
                if file_serializer.is_valid():
                    map_saved = file_serializer.save()
                    map_json = None
                    if 'map' in request.data:
                        map_json = request.data['map']
                    if map_json is not None:
                        save_points_from_json(map_saved, map_json)
                    elif map_saved.file.name is not None:
                        save_points_from_file(map_saved)
                    else:
                        transaction.set_rollback(True)
                        return Response("Could not save map. Send a text file or a json", status=status.HTTP_400_BAD_REQUEST)

                    return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Error in fields:"+e.args.__str__(), status=status.HTTP_400_BAD_REQUEST)
