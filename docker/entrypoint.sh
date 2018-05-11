#!/bin/bash

python /var/www/webapps/certmanager/manage.py migrate
python /var/www/webapps/certmanager/manage.py collectstatic --noinput

/bin/bash -c "$1"
