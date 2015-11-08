from django.test import TestCase

from workflow.models import CSSCase, CSSCall, Verification


class CaseAdmin(TestCase):

    def test_resolve(self):

        report = CSSCall.objects.create()
        verification = Verification.objects.create(report=report)
        case = CSSCase.objects.create(verification=verification)

        self.assertEqual(None, case.resolved_at)

        case.resolve()
        self.assertNotEqual(None, case.resolved_at)
