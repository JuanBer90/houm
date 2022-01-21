
# Houm Challenge

## Problema
En Houm tenemos un gran equipo de Houmers que muestran las propiedades y solucionan todos los problemas que podrían ocurrir en ellas. Ellos son parte fundamental de nuestra operación y de la experiencia que tienen nuestros clientes. Es por esta razón que queremos incorporar ciertas métricas para monitorear cómo operan, mejorar la calidad de servicio y para asegurar la seguridad de nuestros Houmers.



### Requisitos
Crear un servicio REST que:

- Permita que la aplicación móvil mande las coordenadas del Houmer. 
- Para un día retorne todas las coordenadas de las propiedades que visitó y cuanto tiempo se quedó en cada una
- Para un día retorne todos los momentos en que el houmer se trasladó con una velocidad superior a cierto parámetro



Normalmente se pueden obtener estos datos desde una aplicación móvil pero asumo que el desafio esta en calcular la distancia y velocidad.

```
{
     "latitude": -27.0697049, 
     "longitude": -70.8177738,
     "altitude": 9.0,
     "speed": 7.0,
     "time": 1642466925
}

```


### Solucion
Se deben insertar las latitudes, longitudes y hora actual en formato UTC, esta app esta preparada para soportar diferentes
zonas horarias.

# Requisitos

- Ubuntu >= 18.04 LTS

- python3.8

Si no tienes instalado python 3.8 puedes hacerlo siguiendo este tutorial

https://phoenixnap.com/kb/how-to-install-python-3-ubuntu

- python3.8-venv
Si no lo tienes instalado puedes hacerlo ejecutando este comando
``` 
sudo apt install python3.8-venv 
```

# Instalacion
Para ejecutar estos pasos debes estar en la carpeta raiz del proyecto.

1. Crear entorno virtual
``` 
python3.8 -m venv venv
```
3. Activar el entorno virtual
``` 
source venv/bin/activate
```
4. Instalar requirements.txt
``` 
pip install -r requirements.txt
```
5. Crear base de datos y tablas
``` 
python manage.py migrate
```
6. Correr el proyecto
``` 
python manage.py runserver 0.0.0.0:8000
```

# Documentacion

Una vez que el servidor de django de desarrollo este arriba se puede acceder a la documentacion
en el siguiente enlace

http://localhost:8000/swagger/


# Tests
Los tests se encuentran en el package tests/ para ejecutar los mismos debe correr el siguiente comando

``` 
python manage.py test
```



### Docker
Lastimosamente ya no me dio el tiempo de preparar el entorno de produccion en docker :__(
