from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from shortest_route_app.serializers import FileMapSerializer
from shortest_route_app.models import FileMap


class FileMapDetail(APIView):
    """
    Retrieve, update or delete a fileMap instance.
    all the function inside this class have a primary key that make a reference to a specific FileMap
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


