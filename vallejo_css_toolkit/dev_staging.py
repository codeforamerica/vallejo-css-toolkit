from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'debai67alr3fcj',
        'USER': 'orzlptrspgywlw',
        'PASSWORD': '4BuDw4XfuOcsX8-Ddv8kqksQSE',
        'HOST': 'ec2-107-21-223-72.compute-1.amazonaws.com',
        'PORT': ''
    }
}

DEBUG = True

STATIC_LIB_BASE = "/static/libs/"

SETTINGS_EXPORT = [
    'STATIC_LIB_BASE',
]
