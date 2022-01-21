#!/bin/bash

# se obtienen todos los archivos estaticos y se copia en la carpeta definida en settings.STATIC_ROOT
python3 -u manage.py collectstatic --no-input

python3 -u manage.py makemigrations

python3 -u manage.py migrate

workers necesarios
GUNICORN_WORKERS=$(((2*$(nproc))+1))

gunicorn --workers $GUNICORN_WORKERS --bind 0.0.0.0:8000 gcb.wsgi --timeout 60 --graceful-timeout 60 --log-level debug
y