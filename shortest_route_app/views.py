from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http import Http404
from .serializers import FileMapSerializer
from .models import FileMap


class FileMapView(APIView):
    """
    This class contain API handlers to manipulate the file map with methods GET, POST and DELETE
    """
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileMapSerializer
    queryset = FileMap.objects.all()

    def get(self, request, format=None):
        mapsList = FileMap.objects.all()
        result = []
        for map in mapsList:
            result.append("id:"+str(map.id)+"; nome:"+map.name)

        return Response({'maps':result})

    def post(self, request, *args, **kwargs):
        file_serializer = FileMapSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.ValidationError("Can't open file.")


class FileMapDetail(APIView):
    """
    Retrieve, update or delete a fileMap instance.
    """

    def get_object(self, pk):
        try:
            return FileMap.objects.get(pk=pk)
        except FileMap.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fileMap = self.get_object(pk)
        serializer = FileMapSerializer(fileMap)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        fileMap = self.get_object(pk)
        serializer = FileMapSerializer(fileMap, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        fileMap = self.get_object(pk)
        fileMap.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)