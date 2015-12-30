import re
import os
import logging
import traceback
from datetime import datetime, timedelta

import pytz
from twilio.rest import TwilioRestClient

from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from workflow.models import StaffReportNotification, ReportNotification, CSSCall

log = logging.getLogger('consolelogger')
EMAIL_RE = r"[^@]+@[^@]+\.[^@]+"


def send_staff_notifications():
    settings_mod = os.environ.get('DJANGO_SETTINGS_MODULE')
    if settings_mod:
        env = settings_mod.split('.')[-1]
        base_url = {
            'development': 'localhost:8000',
            'staging': 'https://vallejo-css-toolkit-staging.herokuapp.com',
            'prodction': 'https://compass.cityofvallejo.net',
        }.get(env)

        if base_url:
            for staff_report_notification in StaffReportNotification.objects.filter(sent_at__isnull=True):
                if staff_report_notification.to_user.email and staff_report_notification.created_at > pytz.timezone('America/Los_Angeles').localize(datetime.now()) - timedelta(days=7):
                    try:
                        send_mail(
                            'Compass Notification',
                            "{}\n\nYou can view the report here: {}/workflow/report/{}\n\n{}".format(
                                staff_report_notification.message,
                                base_url,
                                staff_report_notification.report.id,
                                staff_report_notification.from_user and '- ' + staff_report_notification.from_user.get_full_name() or '',
                            ),
                            staff_report_notification.from_user and staff_report_notification.from_user.email or 'no-reply@cityofvallejo.net',
                            [staff_report_notification.to_user.email],
                            fail_silently=False
                        )
                        staff_report_notification.sent_at = pytz.timezone('America/Los_Angeles').localize(datetime.now())
                        staff_report_notification.save()
                    except:
                        log.error("Encountered error sending staff email: {}".format(traceback.format_exc()))


def send_public_notifications():
    twilio_client = TwilioRestClient(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
    for report_notification in ReportNotification.objects.filter(sent_at__isnull=True):
        if report_notification.created_at > pytz.timezone('America/Los_Angeles').localize(datetime.now()) - timedelta(days=1):
            if report_notification.report.caller_preferred_contact == CSSCall.EMAIL_CONTACT_PREFERENCE:
                if re.match(EMAIL_RE, report_notification.report.reporter_alternate_contact):
                    try:
                        send_mail(
                            'Compass Notification',
                            "{}\n\nIf you have further questions, please contact Tina Encarnacion at Christina.Encarnacion@cityofvallejo.net".format(report_notification.message),
                            'no-reply@cityofvallejo.net',
                            [report_notification.report.reporter_alternate_contact],
                            fail_silently=False
                        )
                        report_notification.sent_at = pytz.timezone('America/Los_Angeles').localize(datetime.now())
                        report_notification.save()
                    except:
                        log.error("Encountered error sending public email: {}".format(traceback.format_exc()))
            elif report_notification.report.caller_preferred_contact == CSSCall.TEXT_CONTACT_PREFERENCE:
                reporter_phone = report_notification.report.phone and re.sub(r'\D', '', report_notification.report.phone) or ''
                if len(reporter_phone) == 10:
                    try:
                        twilio_client.messages.create(
                            to="+1".format(reporter_phone),
                            from_="+1".format(TWILIO_NUMBER),
                            body="This is an update regarding a report you filed with the City of Vallejo.\n{}".format(report_notification.message)
                        )
                    except:
                        log.error("Encountered error sending public SMS: {}".format(traceback.format_exc()))


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_staff_notifications()
        # send_public_notifications()
