from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vallejo_css_toolkit',
        'USER': 'vallejo_css_toolkit',
        'PASSWORD': 'development',
        'HOST': 'localhost',
        'PORT': ''
    }
}

DEBUG = True

STATIC_LIB_BASE = "/static/libs/"

SETTINGS_EXPORT = [
    'STATIC_LIB_BASE',
]
