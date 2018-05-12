#!/bin/bash

/var/www/webapps/envs/certmanager-DYebl5Cv/bin/python /var/www/webapps/certmanager/manage.py migrate
/var/www/webapps/envs/certmanager-DYebl5Cv/bin/python /var/www/webapps/certmanager/manage.py collectstatic --noinput

/bin/bash -c "$1"
