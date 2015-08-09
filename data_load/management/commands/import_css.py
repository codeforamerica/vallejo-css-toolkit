import csv

from django.core.management.base import BaseCommand

from geo.utils.geocode import geocode
from workflow.models import Case, CaseStatus


def import_css(f):

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
            continue

        if not street_number.isdigit():
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
            description=description,
            resolution=resolution,
            status=closed and closed_status or active_status,
            lat=lat,
            lng=lng
        )

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--file', type=file)

    def handle(self, *args, **options):
        if not options.get('file'):
            return

        import_css(options['file'])
