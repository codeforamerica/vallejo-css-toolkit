from datetime import datetime, timedelta

import pytz

from django.core.management.base import BaseCommand

from workflow.models import StaffReportNotification, CSSCase

DAYS_AGO_CUTOFF = 21


def find_stale_cases():
    cutoff = pytz.timezone('America/Los_Angeles').localize(datetime.now()) - timedelta(days=DAYS_AGO_CUTOFF)

    for unresolved_case in CSSCase.objects.filter(resolved_at__isnull=True):
        if not unresolved_case.caseaction_set.filter(timestamp__gte=cutoff):
            for case_assignee in unresolved_case.csscaseassignee_set.all():
                StaffReportNotification.objects.create(
                    report=unresolved_case.verification.report,
                    message="You're receiving this message because you have an assigned case that has been inactive for more than 21 days.",
                    to_user=case_assignee.assignee_user.user
                )


class Command(BaseCommand):
    def handle(self, *args, **options):
        find_stale_cases()
