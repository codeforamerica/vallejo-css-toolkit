"""
WSGI config for vallejo_css_toolkit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vallejo_css_toolkit.settings")

from dj_static import Cling

application = Cling(get_wsgi_application())
