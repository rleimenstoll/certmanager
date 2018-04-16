#!/bin/bash

python /var/www/webapps/certmanager/manage.py migrate

/bin/bash -c "$1"
