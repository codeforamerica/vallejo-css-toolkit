import os
import re
import sys
import csv
import urllib
import zipfile
import tempfile

from django.core.management.base import BaseCommand

from geo.models import Address

OPEN_ADDRESS_URL = "http://data.openaddresses.io.s3.amazonaws.com/us-ca-solano_county.zip"

EXPECTED_FILENAME = "us-ca-solano_county.csv"

NO_STREET_DESC_RE = "(?P<street_name>(El Sendero|North Camino Alto|Camino Del Sol|Skyway|Loma Vista|Camino Alto|El Verano|El Caminito|El Patio|Pinnacle Point|Bailey)), Vallejo, Ca(, [0-9]{5})?"
STREET_DESC_RE = "(?P<street_name>.*) (?P<street_descriptor>(Wy|Ct|Cir|Rd|St|Dr|Av|Bl|Rl|Ln|Cv|Pl|Ter|Pkwy|Drive East|Drive West|Road E|Avenue E|Road W)), Vallejo, Ca(, [0-9]{5})?"


def import_openaddresses():
    new_imports = 0
    duplicates = 0
    rejects = []

    filename, _ = urllib.urlretrieve(OPEN_ADDRESS_URL)

    td = tempfile.gettempdir()
    zf = zipfile.ZipFile(filename)

    zf.extractall(td)

    with open(os.path.join(td, EXPECTED_FILENAME), 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        for row in reader:
            if len(row) != 5:
                rejects.append(row)
                continue
            else:
                lng, lat, street_number, street_address, zip = row

            if not re.search('Vallejo', street_address):
                continue

            lat = float(lat)
            lng = float(lng)

            if not street_number.isdigit():
                rejects.append(row)
                continue

            street_number = int(street_number)

            # some streets have no descriptor, like 'Broadway'...
            r = re.match(NO_STREET_DESC_RE, street_address)

            if r:
                street_descriptor = None
                street_name = r.groupdict()['street_name']

            else:
                r = re.match(STREET_DESC_RE, street_address)

                if r:
                    street_descriptor = r.groupdict()['street_descriptor']
                    street_name = r.groupdict()['street_name']

                else:
                    rejects.append(row)
                    continue

            _, created = Address.objects.get_or_create(
                street_number=street_number,
                street_name=street_name.lower(),
                street_descriptor=street_descriptor.lower(),
                lat=lat,
                lng=lng
            )

            new_imports += created
            duplicates += created ^ 1

    return new_imports, duplicates, rejects

class Command(BaseCommand):

    def handle(self, *args, **options):
        new_imports, duplicates, rejects = import_openaddresses()

        print 'Imported %d new locations, saw %d duplicates, and rejected the following:' % (new_imports, duplicates)
        for reject in rejects:
            print '\t%s' % reject
