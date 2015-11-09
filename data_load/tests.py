import json
import logging
from datetime import datetime

import pytz

from django.test import TestCase, Client

from data_load.models import RMSCase, CRWCase

TZ = pytz.timezone('America/Los_Angeles')

logging.disable(logging.CRITICAL)


class TestRMSDataLoad(TestCase):

    def setUp(self):
        RMSCase.objects.create(case_no=11500001)

    def test_load_simple(self):
        c = Client()
        c.post(
            '/handle_rms_post/',
            content_type='application/json',
            data=json.dumps([[11500002, '2015-01-01 01:00:00', '459', 'R/P states came home and found home broken into', 2015000001, '117 B ST', '', 'Smith, John']])
        )

        actual_count = RMSCase.objects.count()
        loaded_rms_case = RMSCase.objects.get(case_no=11500002)

        self.assertEqual(actual_count, 2)
        self.assertEqual(loaded_rms_case.date, TZ.localize(datetime(2015, 1, 1, 1, 0)))

    def test_get_latest_case_no(self):
        c = Client()
        response = c.get('/get_latest_rms_case_no/')
        data = json.loads(response.content)

        self.assertEqual(data.get('latest_case_no'), 11500001)

    def tearDown(self):
        for obj in RMSCase.objects.all():
            obj.delete()


class TestCRWDataLoad(TestCase):

    def test_load_simple(self):
        c = Client()
        c.post(
            '/handle_crw_post/',
            content_type='application/json',
            data=json.dumps([['CE', 15, 1, 'CE15-00001', 'Overgrown vegetation', '2015-01-01 01:00:00', 'PMO', 'PROACTIVE', '117', 'B ST', 'JOHN SMITH', 'CLOSED WN']])
        )

        actual_count = CRWCase.objects.count()
        crw_case = CRWCase.objects.get(id=1)

        self.assertEqual(actual_count, 1)
        self.assertEqual(crw_case.started, TZ.localize(datetime(2015, 1, 1, 1, 0)))
