import csv

from django.core.management.base import BaseCommand

from geo.utils.normalize_address import normalize_address_string
from workflow.models import PDCase, CaseLocation

import logging
logger = logging.getLogger('consolelogger')

def process_row(row, commit=False):
    _, address = row

    normalized = normalize_address_string(address)

    if not normalized:
        logger.info('Unable to normalize address: {}'.format(address))
        return

    normalized_street_number, normalized_street_name, normalized_street_descriptor = normalized

    if commit:
        case_location, _ = CaseLocation.objects.get_or_create(
            street_number=normalized_street_number,
            street_name=normalized_street_name,
            street_descriptor=normalized_street_descriptor
        )

        PDCase.objects.get_or_create(
            raw_address=raw_address,
            case_location=case_location
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
