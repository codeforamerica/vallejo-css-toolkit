import csv

import usaddress
from django.core.management.base import BaseCommand

from workflow.models import PDCase


def process_row(row, commit=False):
    _, address = row

    if commit:
        PDCase.objects.get_or_create(
            raw_address=address,
        )

def import_rms(f, commit=False):
    dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
    f.seek(0)
    reader = csv.reader(f, dialect)
    next(reader)

    for row in reader:
        process_row(row, commit)

class Command(BaseCommand):
    # COPY (Select incnum, location from rms_incident where location is not null limit 200) TO '/Users/andrew/Desktop/rms.csv' DELIMITER ',' CSV HEADER;

    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)
        parser.add_argument('--commit', type=bool, default=False)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        import_rms(options['file'], options['commit'])
