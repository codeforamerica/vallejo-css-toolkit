import re
import sys
import csv

from geo.utils.geocode import geocode

from workflow.models import Case, CaseStatus


# query used to generate data file:

# COPY (Select incnum, location from rms_incident where location is not null limit 200) TO '/Users/andrew/Desktop/rms.csv' DELIMITER ',' CSV HEADER;

def import_rms(filepath=None):

    with open(filepath, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        next(reader)

        for i, row in enumerate(reader):
            incnum, address = row

            r = re.match('(?P<street_number>\d*) (?P<street_name>.*)', address)

            if not r:
                print 'no parse: ', address
                continue

            street_number = int(r.groupdict().get('street_number'))
            street_name = r.groupdict().get('street_name')

            lat, lng = None, None

            results = geocode(street_number, street_name.lower())
            if results:
                lat = results[0].get('lat')
                lng = results[0].get('lng')

            # print street_number
            # print street_name, lat, lng

            active_status = CaseStatus.objects.get(name='Active')

            Case.objects.get_or_create(
                # address="%s %s" % (street_number, street_name),
                description='pd call for service',
                resolution='pd call for service',
                status=active_status,
                lat=lat,
                lng=lng,
                dept=1
            )

# TODO: this should be a proper django management command

if __name__ == "__main__":
    import django
    django.setup()

    func_name = sys.argv[1]

    if func_name == 'import_rms':
        filepath = sys.argv[2]
        import_rms(filepath)
