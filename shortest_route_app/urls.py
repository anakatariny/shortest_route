from django.conf.urls import url
from .views import FileMapView, FileMapDetail, MapView

urlpatterns = [
    url(r'^map/$', FileMapView.as_view(), name='file-upload'),
    url(r'^map/(?P<pk>[0-9]+)/$', FileMapDetail.as_view()),
    url(r'^points/$', MapView.as_view()),

]