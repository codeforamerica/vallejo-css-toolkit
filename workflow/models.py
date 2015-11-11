from datetime import datetime

import pytz

from django.db import models
from django.contrib.auth.models import User


class CaseStatus(models.Model):
    name = models.CharField(max_length=256)


class ReportStatus(models.Model):
    name = models.CharField(max_length=256)


# TODO: deprecate
class PDCase(models.Model):
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)


# TODO: deprecate
class CRWCase(models.Model):
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)


class CSSCall(models.Model):
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

    PHONE_SOURCE = 1
    EMAIL_SOURCE = 2
    WEB_SOURCE = 3
    CE_REFERRAL_SOURCE = 4
    OFFICER_REFERRAL_SOURCE = 5
    CITY_REFERRAL_SOURCE = 6

    SOURCE_CHOICES = (
        (PHONE_SOURCE, 'Phone'),
        (EMAIL_SOURCE, 'Email'),
        (WEB_SOURCE, 'Web'),
        (CE_REFERRAL_SOURCE, 'Code Enforcement Referral'),
        (OFFICER_REFERRAL_SOURCE, 'Officer Referral'),
        (CITY_REFERRAL_SOURCE, 'Other City Referral')
    )

    name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256, null=True, blank=True)

    address_number = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=256, null=True, blank=True)
    place_name = models.CharField(max_length=256, null=True, blank=True)

    reporter_address_number = models.IntegerField(null=True, blank=True)
    reporter_street_name = models.CharField(max_length=256, null=True, blank=True)
    reporter_alternate_contact = models.CharField(max_length=256, null=True, blank=True)
    when_last_reported = models.CharField(max_length=256, null=True, blank=True)
    time_of_day_occurs = models.CharField(max_length=256, null=True, blank=True)
    num_people_involved = models.CharField(max_length=256, null=True, blank=True)
    safety_concerns = models.CharField(max_length=256, null=True, blank=True)

    problem = models.CharField(max_length=1024, null=True)
    resolution = models.CharField(max_length=1024, null=True, blank=True)

    # TODO: this should become a proper datetime field
    date = models.CharField(max_length=256, null=True, blank=True)
    reported_datetime = models.DateTimeField(null=True, blank=True)

    tags = models.CharField(max_length=256, null=True, blank=True)

    problem_duration = models.CharField(max_length=256, null=True, blank=True)

    # TODO: we'll eventually need to store geometry objects somewhere
    active = models.BooleanField(default=True)
    caller_preferred_contact = models.IntegerField(null=True, blank=True, choices=CONTACT_PREFERENCES_CHOICES)
    status = models.ForeignKey(ReportStatus, null=True, blank=True)
    source = models.IntegerField(null=True, blank=True, choices=SOURCE_CHOICES)
    call_sid = models.CharField(max_length=256, null=True, blank=True)

    def get_address(self):
        return (self.address_number and self.street_name) and "{} {}".format(self.address_number, self.street_name) or self.address


class Verification(models.Model):
    report = models.ForeignKey(CSSCall)
    property_description = models.CharField(max_length=256, null=True, blank=True)
    owner_name = models.CharField(max_length=256, null=True, blank=True)
    owner_address = models.CharField(max_length=256, null=True, blank=True)
    owner_primary_contact = models.CharField(max_length=256, null=True, blank=True)
    owner_secondary_contact = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    water_service = models.BooleanField(default=False)
    pge_service = models.BooleanField(default=False)
    boarded = models.BooleanField(default=False)
    nlp_assigned = models.BooleanField(default=False)
    code_contacted = models.BooleanField(default=False)
    trespass_letter = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    bank_contact = models.CharField(max_length=256, null=True, blank=True)
    bank_contact_phone = models.CharField(max_length=256, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = pytz.utc.localize(datetime.utcnow())
        super(Verification, self).save(*args, **kwargs)


class VerificationContactAction(models.Model):
    verification = models.ForeignKey(Verification)
    contacter_name = models.CharField(max_length=256, null=True, blank=True)
    contact_type = models.CharField(max_length=256, null=True, blank=True)
    contact_description = models.CharField(max_length=256, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = pytz.utc.localize(datetime.utcnow())
        super(VerificationContactAction, self).save(*args, **kwargs)


class CSSCasePriority(models.Model):
    name = models.CharField(max_length=256)


class CSSCase(models.Model):
    description = models.CharField(max_length=1024, null=True, blank=True)
    resolution = models.CharField(max_length=1024, null=True, blank=True)
    status = models.ForeignKey(CaseStatus, null=True, blank=True)
    address_number = models.IntegerField(null=True, blank=True)
    street_name = models.CharField(max_length=256, null=True, blank=True)
    owner_name = models.CharField(max_length=256, null=True, blank=True)
    owner_address = models.CharField(max_length=256, null=True, blank=True)
    owner_phone = models.CharField(max_length=256, null=True, blank=True)
    owner_email = models.CharField(max_length=256, null=True, blank=True)
    verification = models.ForeignKey(Verification, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    priority = models.ForeignKey(CSSCasePriority, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = pytz.utc.localize(datetime.utcnow())
        super(CSSCase, self).save(*args, **kwargs)

    def resolve(self):
        if not self.resolved_at:
            self.resolved_at = pytz.utc.localize(datetime.utcnow())
        self.save()


class CSSReportView(models.Model):
    css_report = models.ForeignKey(CSSCall)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = pytz.utc.localize(datetime.utcnow())
        super(CSSReportView, self).save(*args, **kwargs)


class Recording(models.Model):
    LOCATION = 1
    DESCRIPTION = 2
    DURATION = 3
    REPORTED_BEFORE = 4
    NAME = 5
    EMAIL = 6
    ADDRESS = 7

    call = models.ForeignKey(CSSCall)
    url = models.CharField(max_length=256, null=True, blank=True)
    type = models.IntegerField(null=True)


class CSSCaseAssignee(models.Model):
    case = models.ForeignKey(CSSCase, null=True, blank=True)
    assignee_name = models.CharField(max_length=256, null=True, blank=True)


class ReportNotification(models.Model):
    report = models.ForeignKey(CSSCall)
    message = models.CharField(max_length=512)
    created_at = models.DateTimeField()
    sent_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = pytz.utc.localize(datetime.utcnow())
        super(ReportNotification, self).save(*args, **kwargs)


class UploadedAsset(models.Model):
    verification = models.ForeignKey(Verification)
    fname = models.CharField(max_length=256, null=True, blank=True)
    fpath = models.CharField(max_length=256, null=True, blank=True)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = pytz.utc.localize(datetime.utcnow())
        super(UploadedAsset, self).save(*args, **kwargs)
