import re
import sys
import csv

from geo.models import Address


def import_openaddresses(filepath=None):

    with open(filepath, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        for row in reader:
            if len(row) == 5:
                lng, lat, street_number, street_address, zip = row
            else:
                pass
                # print 'Invalid line: %s' % row

            if re.search('Vallejo', street_address):


                lat = float(lat)
                lng = float(lng)

                if street_number.isdigit():
                    street_number = int(street_number)
                else:
                    # print 'invalid format for street number: %s' % street_number
                    continue

                r = re.match('(?P<street_name>(El Sendero|North Camino Alto|Camino Del Sol|Skyway|Loma Vista|Camino Alto|El Verano|El Caminito|El Patio|Pinnacle Point|Bailey)), Vallejo, Ca(, [0-9]{5})?', street_address)

                if r:
                    street_descriptor = None
                    street_name = r.groupdict()['street_name']

                else:

                    r = re.match('(?P<street_name>.*) (?P<street_descriptor>(Wy|Ct|Cir|Rd|St|Dr|Av|Bl|Rl|Ln|Cv|Pl|Ter|Pkwy|Drive East|Drive West|Road E|Avenue E|Road W)), Vallejo, Ca(, [0-9]{5})?', street_address)

                    if r:
                        street_descriptor = r.groupdict()['street_descriptor']
                        street_name = r.groupdict()['street_name']

                    else:
                        # print 'unable to parse row: %s' % row
                        continue

                try:
                    Address.objects.get_or_create(
                        street_number=street_number,
                        street_name=street_name,
                        street_descriptor=street_descriptor,
                        lat=lat,
                        lng=lng
                    )
                except:
                    raise

# TODO: this should be a proper django management command

if __name__ == "__main__":

    func_name = sys.argv[1]

    if func_name == 'import_openaddresses':
        filepath = sys.argv[2]
        import_openaddresses(filepath)

    if func_name == 'test_geocode':
        filepath = sys.argv[2]
        test_geocode(filepath)
