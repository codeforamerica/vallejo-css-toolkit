import csv

from django.core.management.base import BaseCommand

from workflow.models import CSSCase, CaseStatus
from geo.utils.normalize_address import combine_address_parts

def process_row(row, commit=False):
    street_number = row[1]
    street_name = row[2]
    description = row[5].strip()
    resolution = row[6].strip()
    closed = row[9]

    if commit:
        closed_status, _ = CaseStatus.objects.get_or_create(name='Closed')
        active_status, _ = CaseStatus.objects.get_or_create(name='Active')

        CSSCase.objects.get_or_create(
            description=description,
            resolution=resolution,
            status=closed and closed_status or active_status,
            raw_address=combine_address_parts(street_number, street_name),
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
