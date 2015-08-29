import csv

import usaddress
from django.core.management.base import BaseCommand

from workflow.models import CSSCase, CaseStatus
# from geo.utils.normalize_address import combine_address_parts

def process_row(row, commit=False):
    address_number = row[1]
    street_name = row[2]
    description = row[5].strip()
    resolution = row[6].strip()
    closed = row[9]

    if commit:
        closed_status, _ = CaseStatus.objects.get_or_create(name='Closed')
        active_status, _ = CaseStatus.objects.get_or_create(name='Active')

        address = "{} {}".format(address_number, street_name)
        tagged = usaddress.tag(address)

        address_type = tagged[1]
        if address_type == 'Street Address':
            address_number = tagged[0].get('AddressNumber')
            street_name = tagged[0].get('StreetName')

            try:
                address_number = int(address_number)
            except ValueError:
                # malformed address_number
                return

            if address_number and street_name:
                CSSCase.objects.get_or_create(
                    description=description,
                    resolution=resolution,
                    status=closed and closed_status or active_status,
                    address_number=address_number,
                    street_name=street_name.upper()
                )

def import_css(f, commit=False):
    dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
    f.seek(0)
    reader = csv.reader(f, dialect)
    next(reader)

    for row in reader:
        process_row(row, commit)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)
        parser.add_argument('--commit', type=bool, default=False)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        import_css(options['file'], options['commit'])
