from django.test import TestCase

from workflow.models import CSSCase


class CaseAdmin(TestCase):

    def test_resolve(self):

        case = CSSCase.objects.create()
        self.assertEqual(None, case.resolved_at)

        case.resolve()
        self.assertNotEqual(None, case.resolved_at)
