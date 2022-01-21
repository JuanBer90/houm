from datetime import timezone, datetime, time
import pytz
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Location
from location.serializers import LocationSerializer
from location.utils import get_datetime_diff, get_daterange_min_max, get_distance


class LocationCreateAPIView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = []

    def post(self, request,*args, **kwargs):
        """
        Se permite que la aplicación móvil mande las coordenadas del Houmer. Ejemplo:
        {
           {
                "latitude": " -25.2692744",
                "longitude": "-57.347477",
                "date_time": "2022-01-21T13:00:00Z"
            }
        }
        """

        return super(LocationCreateAPIView, self).post(request, *args, **kwargs)



class UserTrackingApiView(APIView):

    order_by = '-date_time'

    def get_queryset(self):
        input_date = self.kwargs.get('date')
        # convert string to datetime
        # input_date = datetime.strptime(input_date, '%Y-%m-%d')
        from_date, to_date = get_daterange_min_max(input_date)

        return Location.objects.filter(date_time__range=(from_date, to_date)).order_by(self.order_by)

    def get(self, request, date):
        """
        :param date: El formato de la fecha debe ser yyyy-mm-dd
        :return: Lista las coordenadas de las propiedades que visitó y cuanto tiempo se quedó en cada una.

        """

        queryset = self.get_queryset()
        data = []

        # Se busca la siguiente localizacion, si no existe se asume que aun se encuentra en el mismo sitio
        if queryset.exists():
            try:
                last_location = queryset.first().get_next_by_date_time()
            except:
                last_location = None

            if last_location is not None:
                last_datetime = last_location.date_time
            else:
                last_datetime = datetime.now(tz=timezone.utc)
            for obj in queryset:

                data.append({
                    'id': obj.pk,
                    'date_time': obj.date_time.strftime("%Y-%m-%d %H:%M"),
                    'latitude': obj.latitude,
                    'longitude': obj.longitude,
                    'dwell_time': get_datetime_diff(last_datetime, obj.date_time)
                })
                last_datetime = obj.date_time
        return Response(data)


class UserSpeedApiView(UserTrackingApiView):
    """
     Se separan las APIs porque si se desea la velocidad se requiere de mayor poder computacional
    """
    order_by = 'date_time'

    def get_queryset(self):
        return Location.objects.all().order_by(self.order_by)


    def get(self, request, speed_gt):
        """
            :param speed: Numero decimal que representa una velocidad en km/h. Ejemplo: 10
            :return: Lista las coordenadas de las propiedades que visitó con una velocidad superior al parametro speed

        """

        # Si tuvieramos el dato de la velocidad almacenado seria agregar al queryset  .filter(speed__gt=speed_gt)
        data = []
        locations = self.get_queryset()
        if locations.exists():
            # Se busca la siguiente localizacion, si no existe se asume que aun se encuentra en el mismo sitio
            try:
                previous_location = locations.first().get_previous_by_date_time()
            except:
                previous_location = None
            if previous_location is not None:
                previous_datetime = previous_location.date_time
            else:
                previous_datetime = datetime.now(tz=timezone.utc)
            data = []

            for obj in locations:

                if previous_location is None:
                    speed = 0
                    distance = 0
                else:
                    distance = get_distance(obj.latitude, obj.longitude, previous_location.latitude, previous_location.longitude)
                    if distance > 0:
                        hours = (obj.date_time - previous_datetime ).total_seconds()/3600
                        speed = round(distance/hours, 2)
                    else:
                        speed = 0
                if speed > speed_gt:
                    data.append({
                        'id': obj.pk,
                        'date_time': obj.date_time.strftime("%Y-%m-%d %H:%M"),
                        'latitude': obj.latitude,
                        'longitude': obj.longitude,
                        'speed': f'{speed} km/h',
                        'distance': f'{distance < 1 and distance * 1000 or distance } {distance >= 1 and "Km" or "m"}',
                        'dwell_time': get_datetime_diff(obj.date_time, previous_datetime )
                    })
                previous_datetime = obj.date_time
                previous_location = obj
        return Response(data)