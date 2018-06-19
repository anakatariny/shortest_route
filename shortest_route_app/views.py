from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileMapSerializer
from .models import FileMap

class FileMapView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileMapSerializer
    queryset = FileMap.objects.all()

    def get(self, request, format=None):
        mapsList = FileMap.objects.all()
        return Response({'maps':mapsList})

    def post(self, request, *args, **kwargs):
        file_serializer = FileMapSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)