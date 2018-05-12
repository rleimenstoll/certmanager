import os

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['Certmanager__DB_HOST'],
        'USER': os.environ['Certmanager__DB_USER'],
        'NAME': os.environ['Certmanager__DB_NAME'],
        'PASSWORD': os.environ['Certmanager__DB_PASSWORD'],
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}


CELERY_BROKER_TRANSPORT = 'sqs'

CELERY_BROKER_URL = 'sqs://'

CELERY_DEFAULT_QUEUE = os.environ['Certmanager__DEFAULT_QUEUE']
