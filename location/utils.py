from datetime import datetime, timedelta, time, timezone
import math

from location.models import Location


def get_datetime_diff(datetime1: datetime, datetime2: datetime):
    """
    :param datetime1: hora y fecha final
    :param datetime2: hora y fecha inicial
    :return: diferencia en dias, horas y minutos
    """
    def plural(n):
        return n, abs(n) != 1 and "s" or ""

    dwell_time = datetime1 - datetime2
    mm, ss = divmod(dwell_time.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%d minuto%s" % (plural(mm))
    if hh > 0:
        s = "%d hora%s y " % (plural(hh))+s
    if dwell_time.days:
        s = ("%d día%s, " % plural(dwell_time.days)) + s
    return s


def get_daterange_min_max(my_date: datetime):
    # combine `from_date` with min time value (00:00)
    from_date = datetime.combine(my_date, time.min).replace(tzinfo=timezone.utc)
    # combine `from_date` with max time value (23:59:99) to have end date
    to_date = datetime.combine(my_date, time.max).replace(tzinfo=timezone.utc)
    return from_date, to_date


def get_distance(lat1, lon1, lat2, lon2):
    """
    Obtiene la distancia en km entre entre dos puntos de
    coordenadas geograficas P1 a P2
    """

    #  Conversion de GMS a DEC y posteriormente a radianes
    lat1rad = math.radians(lat1)
    lon1rad = math.radians(lon1)

    lat2rad = math.radians(lat2)
    lon2rad = math.radians(lon2)

    #  Si las latitudes y longitudes son iguales se encuentran en el mismo sitio geografico
    if lat1rad == lat2rad and lon1rad == lon2rad:
        return 0

    #  Calculo de la distancia P1 a P2
    a = math.sin(lat1rad)*math.sin(lat2rad)
    b = math.cos(lat1rad)*math.cos(lat2rad)*math.cos(lon2rad - lon1rad)
    D = math.acos(a + b)  # Formula (2)

    d = 111.18*math.degrees(D)  # Formula (1)
    # distancia en metros
    return round(d, 2)
