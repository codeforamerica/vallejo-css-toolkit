import csv
from datetime import datetime

import pytz

# import usaddress
from django.core.management.base import BaseCommand

from workflow.models import CSSCall

tz = pytz.timezone('America/Los_Angeles')
UTC = pytz.utc


def process_row(row, commit=False):

    if not row:
        return

    name, address, phone, problem, date, resolution = row

    date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d')).astimezone(UTC)

    # try:
    #     tagged = usaddress.tag(address)
    # except usaddress.RepeatedLabelError:
    #     return

    # address_type = tagged[1]
    # if address_type == 'Street Address':
    #     address_number = tagged[0].get('AddressNumber')
    #     street_name = tagged[0].get('StreetName')

    #     try:
    #         address_number = int(address_number)
    #     except ValueError:
    #         # malformed address_number
    #         return

    #     if address_number and street_name:

    if commit:
        CSSCall.objects.get_or_create(
            name=name,
            address=address,
            phone=phone,
            problem=problem,
            reported_datetime=date_converted,
            resolution=resolution
        )


def process_csv(f, commit=False):
    dialect = csv.Sniffer().sniff(f.read(104857600), delimiters="\t")
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

        process_csv(options['file'], options['commit'])
