from datetime import datetime

import pytz

from django.test import TestCase

from workflow.models import CSSCall
from common.datatables import get_datatables_data
from workflow.views.report_views import CALLS_IDX_COLUMN_MAP
from workflow.sql import CALLS_DATA_SQL

TZ = pytz.timezone('America/Los_Angeles')

request_dict = {
    "draw": "1",
    "columns[0][data]": "0",
    "columns[0][name]": "",
    "columns[0][searchable]": "false",
    "columns[0][orderable]": "true",
    "columns[0][search][value]": "",
    "columns[0][search][regex]": "false",
    "columns[1][data]": "1",
    "columns[1][name]": "",
    "columns[1][searchable]": "true",
    "columns[1][orderable]": "true",
    "columns[1][search][value]": "",
    "columns[1][search][regex]": "false",
    "columns[2][data]": "2",
    "columns[2][name]": "",
    "columns[2][searchable]": "true",
    "columns[2][orderable]": "true",
    "columns[2][search][value]": "",
    "columns[2][search][regex]": "false",
    "columns[3][data]": "3",
    "columns[3][name]": "",
    "columns[3][searchable]": "true",
    "columns[3][orderable]": "true",
    "columns[3][search][value]": "",
    "columns[3][search][regex]": "false",
    "columns[4][data]": "4",
    "columns[4][name]": "",
    "columns[4][searchable]": "true",
    "columns[4][orderable]": "true",
    "columns[4][search][value]": "",
    "columns[4][search][regex]": "false",
    "columns[5][data]": "5",
    "columns[5][name]": "",
    "columns[5][searchable]": "true",
    "columns[5][orderable]": "true",
    "columns[5][search][value]": "",
    "columns[5][search][regex]": "false",
    "columns[6][data]": "6",
    "columns[6][name]": "",
    "columns[6][searchable]": "true",
    "columns[6][orderable]": "true",
    "columns[6][search][value]": "",
    "columns[6][search][regex]": "false",
    "columns[7][data]": "7",
    "columns[7][name]": "",
    "columns[7][searchable]": "false",
    "columns[7][orderable]": "true",
    "columns[7][search][value]": "",
    "columns[7][search][regex]": "false",
    "columns[8][data]": "8",
    "columns[8][name]": "",
    "columns[8][searchable]": "false",
    "columns[8][orderable]": "true",
    "columns[8][search][value]": "",
    "columns[8][search][regex]": "false",
    "columns[9][data]": "9",
    "columns[9][name]": "",
    "columns[9][searchable]": "false",
    "columns[9][orderable]": "true",
    "columns[9][search][value]": "",
    "columns[9][search][regex]": "false",
    "order[0][column]": "7",
    "order[0][dir]": "desc",
    "start": "0",
    "length": "2",
    "search[value]": "",
    "search[regex]": "false",
    "_": "1441321395643"
}


class DatatablesTestCase(TestCase):
    def setUp(self):

        for i in xrange(0, 4):
            CSSCall.objects.create(
                name="Fake Name {}".format(i),
                address="{} Fake Street".format(i),
                phone="{}{}{}-{}{}{}{}".format(i, i, i, i, i, i, i),
                problem="Problem #{}".format(i),
                reported_datetime=TZ.localize(datetime(2015, 9, i + 1, 12, 0, 0)),
                resolution="Some resoltuion #{}".format(i)
            )

    def test_data_fetch(self):

        self.maxDiff = None

        """Base case test that GET query params passed from datatables are properly handled."""

        results = get_datatables_data(request_dict, CALLS_DATA_SQL, CALLS_IDX_COLUMN_MAP)

        expected_results = {
            'recordsFiltered': 4,
            'recordsTotal': 4,
            'data': [
                (
                    4,
                    datetime(2015, 9, 4, 12, 0),
                    u'<a href="/workflow/report/4">2015-09-04 12:00</a>',
                    u'Fake Name 3',
                    u'<a href="/workflow/report/4">Fake Name 3</a>',
                    u'333-3333',
                    u'<a href="/workflow/report/4">333-3333</a>',
                    u'3 Fake Street',
                    u'<a href="/workflow/report/4">3 Fake Street</a>',
                    u'Problem #3',
                    u'<a href="/workflow/report/4">Problem #3</a>',
                    u'Some resoltuion #3',
                    u'<a href="/workflow/report/4">Some resoltuion #3</a>',
                    4L,
                    4L
                ),
                (
                    3,
                    datetime(2015, 9, 3, 12, 0),
                    u'<a href="/workflow/report/3">2015-09-03 12:00</a>',
                    u'Fake Name 2',
                    u'<a href="/workflow/report/3">Fake Name 2</a>',
                    u'222-2222',
                    u'<a href="/workflow/report/3">222-2222</a>',
                    u'2 Fake Street',
                    u'<a href="/workflow/report/3">2 Fake Street</a>',
                    u'Problem #2',
                    u'<a href="/workflow/report/3">Problem #2</a>',
                    u'Some resoltuion #2',
                    u'<a href="/workflow/report/3">Some resoltuion #2</a>',
                    4L,
                    4L
                )
            ]
        }

        self.assertEqual(results, expected_results)
