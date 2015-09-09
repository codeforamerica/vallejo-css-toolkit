import csv

import usaddress
from django.core.management.base import BaseCommand

from workflow.models import PDCase


def process_row(row, commit=False):
    try:
        address = row[25]
    except IndexError:
        return

    try:
        tagged = usaddress.tag(address)
    except usaddress.RepeatedLabelError:
        return

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
            if commit:
                PDCase.objects.get_or_create(
                    address_number=address_number,
                    street_name=street_name.upper()
                )

def process_csv(f, commit=False, delete_existing=False):
    dialect = csv.Sniffer().sniff(f.read(), delimiters=",")
    f.seek(0)
    reader = csv.reader(f, dialect)
    # next(reader)

    print commit, delete_existing
    if commit and delete_existing:
        PDCase.objects.all().delete()

    for row in reader:
        # print row
        process_row(row, commit)        

class Command(BaseCommand):
    # COPY (Select incnum, location from rms_incident where location is not null limit 200) TO '/Users/andrew/Desktop/rms.csv' DELIMITER ',' CSV HEADER;

    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)
        parser.add_argument('--commit', type=bool, default=False)
        parser.add_argument('--delete_existing', type=bool, default=False)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        process_csv(options['file'], options['commit'], options['delete_existing'])
