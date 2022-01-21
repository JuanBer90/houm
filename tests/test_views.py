
from django.urls import reverse

from location.models import Location
from .test_setup import TestSetUp


class TestViews(TestSetUp):

    def test_insert_coordinates_with_no_data(self):
        res = self.client.post(self.insert_url)
        self.assertEqual(res.status_code, 400)

    def test_insert_coordinate(self):
        for coordinate in self.coordinates:
            res = self.client.post(self.insert_url, coordinate, format="json")
            self.assertEqual(res.status_code, 201)
            self.assertEqual(res.data['latitude'], coordinate['latitude'], msg="Las latitudes no coinciden")
            self.assertEqual(res.data['longitude'], coordinate['longitude'], msg="Las longitudes no coinciden")
            self.assertEqual(res.data['date_time'], coordinate['date_time'], msg="Las fechas no coinciden")

        queryset = Location.objects.filter(latitude=self.coordinates[0]["latitude"], longitude=self.coordinates[0]["longitude"])
        self.assertTrue(queryset.exists(), msg="No existe un lugar con las coordenadas proveidas")


    def test_speed(self):
        print("Testing: Momentos en que el houmer se trasladó con una velocidad superior a cierto parámetro...")
        for coordinate in self.coordinates:
            self.client.post(self.insert_url, coordinate, format="json")

        res = self.client.get(self.speed_coordinates_url, format="json")
        self.assertEqual(len(res.data), 2,
                         msg="La cantidad de coordenadas que superan la velocidad de 15 km/h debe ser 2")


    def test_dwell_time(self):
        print("Testing: Todas las coordenadas de las propiedades que visitó y cuanto tiempo se quedó en cada una...")
        for coordinate in self.coordinates:
            self.client.post(self.insert_url, coordinate, format="json")

        dwell_time_url_date1 = reverse('dwell_time-coordinates', kwargs={'date': '2022-01-21'})
        res1 = self.client.get(dwell_time_url_date1, format="json")
        self.assertEqual(len(res1.data), 1,
                         msg="La cantidad de lugares que visito debe ser 1")


        dwell_time_url_date2 = reverse('dwell_time-coordinates', kwargs={'date': '2022-01-22'})
        res2 = self.client.get(dwell_time_url_date2, format="json")
        self.assertEqual(len(res2.data), 3,
                         msg="La cantidad de lugares que visito debe ser 3")


        dwell_time_url_date3 = reverse('dwell_time-coordinates', kwargs={'date': '2022-01-23'})
        res3 = self.client.get(dwell_time_url_date3, format="json")
        self.assertEqual(len(res3.data), 1,
                         msg="La cantidad de lugares que visito debe ser 1")

        dwell_time_url_date4 = reverse('dwell_time-coordinates', kwargs={'date': '2022-01-24'})
        res3 = self.client.get(dwell_time_url_date4, format="json")
        self.assertEqual(len(res3.data), 0,
                         msg="No se visitaron lugares en este dia")


