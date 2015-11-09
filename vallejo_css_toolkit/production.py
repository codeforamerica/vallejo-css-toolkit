import dj_database_url

from .settings import *

DATABASES = {'default': dj_database_url.config()}
DEBUG = False

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_LIB_BASE = "https://s3.amazonaws.com/vallejo-css-toolkit/static/libs/"

SETTINGS_EXPORT = [
    'STATIC_LIB_BASE',
]
