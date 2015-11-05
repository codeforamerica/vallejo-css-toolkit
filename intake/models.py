import datetime

from django.db import models
from django.contrib.auth.models import User
from workflow.models import CSSCall

UNREVIEWED_STATUS = 1
ACTIVE_STATUS = 2
CLOSED_STATUS = 3
SUSPENDED_STATUS = 4

STATUS_CHOICES = (
    (UNREVIEWED_STATUS, 'Unreviewed'),
    (ACTIVE_STATUS, 'Active'),
    (CLOSED_STATUS, 'Closed'),
    (SUSPENDED_STATUS, 'Suspended'),
)

NO_CONTACT_PREFERENCE = 1
TEXT_CONTACT_PREFERENCE = 2
CALL_CONTACT_PREFERENCE = 3
EMAIL_CONTACT_PREFERENCE = 4

CONTACT_PREFERENCES_CHOICES = (
    (NO_CONTACT_PREFERENCE, 'No Contact'),
    (NO_CONTACT_PREFERENCE, 'Text'),
    (CALL_CONTACT_PREFERENCE, 'Call'),
    (EMAIL_CONTACT_PREFERENCE, 'Email'),
)


class Call(models.Model):
    call_sid = models.CharField(max_length=256, null=True)
    caller_name = models.CharField(max_length=256, null=True, blank=True)
    name_recording_url = models.CharField(max_length=256, null=True, blank=True)

    caller_number = models.CharField(max_length=256, null=True, blank=True)
    call_time = models.DateTimeField(null=True)

    caller_preferred_contact = models.IntegerField(null=True, blank=True, choices=CONTACT_PREFERENCES_CHOICES)

    problem_address = models.CharField(max_length=256, null=True, blank=True)
    address_recording_url = models.CharField(max_length=256, null=True, blank=True)

    problem_description = models.TextField(max_length=1024, null=True, blank=True)
    description_recording_url = models.CharField(max_length=256, null=True, blank=True)

    resolution = models.CharField(max_length=256, null=True, blank=True)

    status = models.IntegerField(null=True, blank=True, choices=STATUS_CHOICES)
    assignee = models.ForeignKey(User, null=True, blank=True)
    property_owner = models.CharField(max_length=256, null=True, blank=True)
    property_owner_phone = models.BigIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.call_time:
            self.call_time = datetime.datetime.utcnow()
        super(Call, self).save(*args, **kwargs)


class TypeformAsset(models.Model):
    css_report = models.ForeignKey(CSSCall)
    asset_url = models.CharField(max_length=256, null=True, blank=True)


class CallAuditItem(models.Model):
    user = models.ForeignKey(User)
    call = models.ForeignKey(Call)
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_field = models.CharField(max_length=256, null=True, blank=True)
    old_value = models.CharField(max_length=256, null=True, blank=True)
    new_value = models.CharField(max_length=256, null=True, blank=True)


class TypeformSubmission(models.Model):
    typeform_json = models.TextField(null=True)
