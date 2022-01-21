from datetime import time, timedelta

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime


class Location(models.Model):
    """
     Este modelo almacena la latitud y longitud que se manda a la API y la fecha y hora en que fueron almacenados
     los datos.

    """
    # user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuario')
    latitude = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='Latitud',
                                   help_text="Maximo 7 decimales. Ej: -27.0697049")
    longitude = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='Longitud',
                                    help_text="Maximo 7 decimales. Ej: -70.8177738")
    date_time = models.DateTimeField(verbose_name='Fecha y Hora', default=datetime.utcnow,
                                     help_text="Probando si sale el help text")

    def __str__(self):
        return f'{self.latitude},{self.longitude}'



