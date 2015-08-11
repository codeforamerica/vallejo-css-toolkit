import os

from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger('consolelogger')

def remove_migrations():
    cwd = os.getcwd()
    for app_name in ('data_load', 'geo', 'intake', 'workflow'):
        dirpath = os.path.join(cwd, app_name, 'migrations')
        for filepath in os.listdir(dirpath):
            if filepath != '__init__.py':
                to_remove = os.path.join(dirpath, filepath)
                os.remove(to_remove)
                logger.info('removed {}'.format(to_remove))

class Command(BaseCommand):

    def handle(self, *args, **options):
        remove_migrations()
