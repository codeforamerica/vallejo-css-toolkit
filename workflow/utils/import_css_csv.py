import re
import sys
import csv

from geo.utils.geocode import geocode

from workflow.models import Case, CaseStatus


def import_css_csv(filepath=None):

    with open(filepath, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1048576), delimiters=",")
        f.seek(0)
        reader = csv.reader(f, dialect)

        next(reader)

        for i, row in enumerate(reader):
            street_number = row[1]
            street_name = row[2]
            description = row[5].strip()
            resolution = row[6].strip()
            closed = row[9]

            if not street_number and street_name:
                # print 'bad row: ', row
                continue

            if not street_number.isdigit():
                # print 'bad street_number: ', street_number
                continue

            street_number = int(street_number)

            lat, lng = None, None

            results = geocode(street_number, street_name)
            if results:
                lat = results[0].get('lat')
                lng = results[0].get('lng')

            closed_status = CaseStatus.objects.get(name='Closed')
            active_status = CaseStatus.objects.get(name='Active')

            Case.objects.get_or_create(
                # address="%s %s" % (street_number, street_name),
                description=description,
                resolution=resolution,
                status=closed and closed_status or active_status,
                lat=lat,
                lng=lng
            )

# TODO: this should be a proper django management command

if __name__ == "__main__":
    import django
    django.setup()

    func_name = sys.argv[1]

    if func_name == 'import_css_csv':
        filepath = sys.argv[2]
        import_css_csv(filepath)
