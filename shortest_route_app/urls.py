from django.conf.urls import url
from .views import FileMapView
urlpatterns = [
  url(r'^map/$', FileMapView.as_view(), name='file-upload'),
]