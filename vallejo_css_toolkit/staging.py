import dj_database_url

from .settings import *

DATABASES = {'default': dj_database_url.config()}
DEBUG = True

STATIC_LIB_BASE = "https://s3.amazonaws.com/vallejo-css-toolkit/static/libs/"

SETTINGS_EXPORT = [
    'STATIC_LIB_BASE',
]
