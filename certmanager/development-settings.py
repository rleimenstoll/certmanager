DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/srv/db/db.sqlite3'
    }
}

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'
