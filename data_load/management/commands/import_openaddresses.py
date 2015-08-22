import os
import re
import csv
import urllib
import logging
import zipfile
import tempfile

from django.core.management.base import BaseCommand
import usaddress

from geo.models import LocationPosition
from geo.utils.normalize_address import normalize_address_by_number_and_street


OPEN_ADDRESS_URL = "http://data.openaddresses.io.s3.amazonaws.com/us-ca-solano_county.zip"
EXPECTED_FILENAME = "us-ca-solano_county.csv"
VALLEJO_LINE_MATCH = "(?P<street_name>.*), Vallejo, Ca(, [0-9]{5})?"

logger = logging.getLogger('consolelogger')

def process_row(row, commit=False):

    if len(row) != 5:
        logger.info('Rejecting row because it does not contain 5 columns: {}'.format(row))
        return

    else:
        lng, lat, street_number, street_address, zipcode = row

    r = re.match(VALLEJO_LINE_MATCH, street_address)
    if not r:
        return

    street_name = r.groupdict()['street_name']

    lat = float(lat)
    lng = float(lng)

    if not street_number.isdigit():
        logger.info('Rejecting row because street number is not numeric: {}'.format(row))
        return

    street_number = int(street_number)
    normalized = normalize_address_by_number_and_street(street_number, street_name)

    if not normalized:
        logger.info('Rejecting row because address could not be normalized: {}'.format(row))
        return

    street_number, street_name, street_descriptor = normalized

    if commit:

        _, created = LocationPosition.objects.get_or_create(
            street_number=street_number,
            street_name=street_name,
            street_descriptor=street_descriptor,
            lat=lat,
            lng=lng,
        )

        return created

def import_openaddresses(commit=False):
    new_imports = 0
    total = 0

    filename, _ = urllib.urlretrieve(OPEN_ADDRESS_URL)

    td = tempfile.gettempdir()
    zf = zipfile.ZipFile(filename)
    zf.extractall(td)

    with open(os.path.join(td, EXPECTED_FILENAME), 'rb') as f:
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

    def handle(self, *args, **options):
        commit = options.get('commit')
        new_imports, total = import_openaddresses(commit)

        logger.info('Imported %d new locations of %d total' % (new_imports, total))
