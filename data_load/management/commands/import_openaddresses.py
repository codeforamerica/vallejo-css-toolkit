import os
import re
import csv
import urllib
import logging
import zipfile
import tempfile

import usaddress
from django.core.management.base import BaseCommand

from geo.models import LocationPosition


OPEN_ADDRESS_URL = "http://data.openaddresses.io.s3.amazonaws.com/us-ca-solano_county.zip"
EXPECTED_FILENAME = "us-ca-solano_county.csv"
VALLEJO_LINE_MATCH = "(?P<street_name>.*), Vallejo, Ca(, [0-9]{5})?"

logger = logging.getLogger('consolelogger')


def process_row(row, commit=False):

    if len(row) != 5:
        logger.info('Rejecting row because it does not contain 5 columns: {}'.format(row))
        return

    else:
        lng, lat, address_number, street_address, zipcode = row

    r = re.match(VALLEJO_LINE_MATCH, street_address)
    if not r:
        return

    address = "{} {}".format(address_number, street_address)
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


def import_openaddresses(commit=False, filepath=''):
    new_imports = 0
    total = 0

    if filepath:
        fpath = filepath
    else:
        filename, _ = urllib.urlretrieve(OPEN_ADDRESS_URL)
        td = tempfile.gettempdir()
        zf = zipfile.ZipFile(filename)
        zf.extractall(td)
        fpath = os.path.join(td, EXPECTED_FILENAME)

    with open(fpath, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        for row in reader:
            total += 1
            result = process_row(row, commit)
            if result:
                new_imports += result

    return new_imports, total


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--commit', type=bool, default=False)
        parser.add_argument('--filepath', type=str)

    def handle(self, *args, **options):
        commit = options.get('commit')
        filepath = options.get('filepath')
        new_imports, total = import_openaddresses(commit, filepath)

        logger.info('Imported %d new locations of %d total' % (new_imports, total))
