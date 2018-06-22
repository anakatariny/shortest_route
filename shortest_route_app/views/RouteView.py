from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from shortest_route_app.models import FileMap, Map, Route
from shortest_route_app.serializers.RouteSerializer import RouteSerializer
from shortest_route_app.utils.Dijsktra import Dijsktra
from shortest_route_app.utils.Graph import Graph
from shortest_route_app.utils.Utils import is_number


@api_view(['GET'])
def get_shortest_route(request, map_name, origin, destination, fuel_autonomy, fuel_cost):
    """Busca menor rota (distância) e calcula seu custo de combustivel dado a autonomia do veículo"""

    try:
        map = FileMap.objects.get(name=map_name)
    except FileMap.DoesNotExist:
        return Response('No map with this name was found.', status=status.HTTP_400_BAD_REQUEST)
    # note: checking origin and destination as first and second edges because is bidirectional
    if not Map.objects.filter(Q(first_edge=origin) | Q(second_edge=origin)).exists():
        return Response('Point of origin not found on the map.', status=status.HTTP_400_BAD_REQUEST)

    if not Map.objects.filter(Q(second_edge=destination) | Q(first_edge=destination)).exists():
        return Response('Point of destination not found on the map.', status=status.HTTP_400_BAD_REQUEST)

    if not is_number(fuel_autonomy):
        return Response('Fuel autonomy must be a number.', status=status.HTTP_400_BAD_REQUEST)

    if not is_number(fuel_cost):
        return Response('Fuel cost must be a number.', status=status.HTTP_400_BAD_REQUEST)
    # checks if the route is in the cache, if true just return the route, else calculates a shortest route
    cached_route = (Route.objects.filter(file_id=map, origin=origin, destination=destination) | \
                   Route.objects.filter(file_id=map, origin=destination, destination=origin)).first()
    if cached_route is not None:
        cost = (cached_route.distance/float(fuel_autonomy))*float(fuel_cost)
        return Response('best_route:' + cached_route.minimum_route + '; cost:' + str(cost) + '; Route in Cache!!!!')
    else:
        paths = Map.objects.filter(file_id__name=map_name)
        graph = Graph()
        for path in paths:
            edge = path.get_edge()
            graph.add_edge(*edge)
        best_route = Dijsktra(graph, origin, destination)
        cost = 0
        dist = 0
        # if find a route returns a list
        if type(best_route) == list:
            # get the last element in the list because the distance is there
            dist = best_route[-1]
            cost = (dist/float(fuel_autonomy))*float(fuel_cost)
            del best_route[-1]
        # save the result in cache
        cache_result = Route.objects.create(file_id=map, origin=origin, destination=destination,
                                          minimum_route=str(best_route), distance=dist)
        cache_result.save()
        return Response('best_route:' + str(best_route) + '; cost:' + str(cost) + '; Route from New Route!!!!')


class RouteView(APIView):
    """
    This class contain API handlers to manipulate the class map in database with methods GET, POST and DELETE
    """
    serializer_class = RouteSerializer
    queryset = Route.objects.all()

    def get(self, request, format=None):
        routes_list = Route.objects.all()
        # get all the map fields
        result = []
        for route in routes_list:
            result.append("map_id:" + route.file_id.name + "; origin:" + route.origin + "; destination:" +
                          route.destination + "; path:" + route.minimum_route + "; distance:" + str(route.distance))

        return Response({'routes': result})




