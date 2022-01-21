from datetime import datetime

from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

class TestSetUp(APITestCase):


    def setUp(self)-> None:
        self.insert_url = reverse('insert-coordinates')

        self.speed_coordinates_url = reverse('speed-coordinates', kwargs={'speed_gt': 15})
        self.coordinates = [
            {
                "latitude": "-25.2692744",
                "longitude": "-57.3474770",
                "date_time": "2022-01-21T13:00:00Z"
            },
            {
                "latitude": "-25.3496650",
                "longitude": "-57.4738427",
                "date_time": "2022-01-22T13:00:00Z"
            },
            {
                "latitude": "-25.3595931",
                "longitude": "-57.5085612",
                "date_time": "2022-01-22T13:10:00Z"
            },
            {
                "latitude": "-25.5067602",
                "longitude": "-57.3788079",
                "date_time": "2022-01-22T14:17:00Z"
            },
            {
                "latitude": "-26.1224566",
                "longitude": "-54.8263893",
                "date_time": "2022-01-23T14:17:00Z"
            }

        ]

    def tearDown(self) -> None:
        return super(TestSetUp, self).tearDown()