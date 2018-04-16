import os

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.environ['Certmanager__DB_USER'],
        'NAME': os.environ['Certmanager__DB_NAME'],
        'PASSWORD': os.environ['Certmanager__DB_PASSWORD'],
    }
}
