from django.urls import path, re_path

from shortest_route_app.views.RouteView import get_shortest_route, RouteView
from .views import FileMapView, FileMapDetail, MapView

urlpatterns = [
    path('map/', FileMapView.as_view()),
    path('map/<int:pk>/', FileMapDetail.as_view()),
    path('points/', MapView.as_view()),
    path('routes/', RouteView.as_view()),
    # this expression redirects to the shortest route function and calculates the best path. The cost is calculated
    # with the extra data passed in this url (car autonomy, origin, fuel cost)
    re_path(r'shortest_route/(?P<map_name>\w+)/(?P<origin>\w+)/(?P<destination>\w+)/(?P<fuel_autonomy>\d+(\.\d+)?)/'
            r'(?P<fuel_cost>\d+(\.\d+)?)/',get_shortest_route)
]

