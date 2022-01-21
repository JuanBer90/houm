from django.urls import path, re_path, include, register_converter
from rest_framework import routers

from location.views import LocationCreateAPIView, UserTrackingApiView, UserSpeedApiView
from datetime import datetime
router = routers.DefaultRouter()

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('api/location/', LocationCreateAPIView.as_view(), name="insert-coordinates"),
    path('api/location/tracking/<yyyy:date>/', UserTrackingApiView.as_view(), name="dwell_time-coordinates"),
    path('api/location/speed/<int:speed_gt>/', UserSpeedApiView.as_view(), name="speed-coordinates"),

]
