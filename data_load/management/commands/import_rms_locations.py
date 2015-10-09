import csv

import usaddress
from django.core.management.base import BaseCommand

from geo.models import LocationPosition


def process_row(row, commit=False):
    try:
        address = row[0]
        lng = row[2]
        lat = row[3]
    except IndexError:
        print row
        return

    tagged = usaddress.tag(address)

    address_type = tagged[1]
    if address_type == 'Street Address':
        address_number = tagged[0].get('AddressNumber')
        street_name = tagged[0].get('StreetName')

        if address_number and street_name:
            try:
                lat = float(lat)
                lng = float(lng)
                address_number = int(address_number)
            except ValueError:
                # malformed lat and/or lng
                return

            if commit:
                LocationPosition.objects.get_or_create(
                    address_number=address_number,
                    street_name=street_name.upper(),
                    lng=lng,
                    lat=lat
                )

def process_csv(f, commit=False):
    dialect = csv.Sniffer().sniff(f.read(1073741824), delimiters=",")
    f.seek(0)
    reader = csv.reader(f, dialect)
    next(reader)

    for row in reader:
        # print row
        process_row(row, commit)        

class Command(BaseCommand):
    # COPY (Select incnum, location from rms_incident where location is not null limit 200) TO '/Users/andrew/Desktop/rms.csv' DELIMITER ',' CSV HEADER;

    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)
        parser.add_argument('--commit', type=bool, default=False)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        process_csv(options['file'], options['commit'])
