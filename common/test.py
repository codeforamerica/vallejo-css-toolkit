from django.test import TestCase

from workflow.models import CSSCall
from common.datatables import get_datatables_data
from workflow.views.call_views import CALLS_IDX_COLUMN_MAP
from workflow.sql import CALLS_DATA_SQL


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

class GeocodeTestCase(TestCase):
    def setUp(self):

        for i in xrange(0, 4):
            CSSCall.objects.create(
                name="Fake Name {}".format(i),
                address="{} Fake Street".format(i),
                phone="{}{}{}-{}{}{}{}".format(i, i, i, i, i, i, i),
                problem="Problem #{}".format(i),
                date="9/{}/2015".format(i),
                resolution="Some resoltuion #{}".format(i)
            )

    def test_geocode_exact(self):
        """Base case test that GET query params passed from datatables are properly handled."""

        results = get_datatables_data(request_dict, CALLS_DATA_SQL, CALLS_IDX_COLUMN_MAP)
        expected_results = {
            'recordsFiltered': 4,
            'recordsTotal': 4,
            'data': [
                ('<a href="/workflow/call/4">4</a>', '9/3/2015', 'Fake Name 3', '333-3333', '3 Fake Street', 'Problem #3', 'Some resoltuion #3', 4, 4, 4),
                ('<a href="/workflow/call/3">3</a>', '9/2/2015', 'Fake Name 2', '222-2222', '2 Fake Street', 'Problem #2', 'Some resoltuion #2', 3, 4, 4)
            ]
        }

        self.assertEqual(results, expected_results)
