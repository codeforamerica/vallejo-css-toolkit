from django.db import models


class CaseStatus(models.Model):
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


class PDCase(models.Model):
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)


class CRWCase(models.Model):
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)


class CSSCall(models.Model):
    name = models.CharField(max_length=256, null=True)
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

    problem = models.CharField(max_length=256, null=True, blank=True)
    resolution = models.CharField(max_length=256, null=True, blank=True)

    # TODO: this should become a proper datetime field
    date = models.CharField(max_length=256, null=True, blank=True)
    reported_datetime = models.DateTimeField(null=True, blank=True)

    tags = models.CharField(max_length=256, null=True, blank=True)

    problem_duration = models.CharField(max_length=256, null=True, blank=True)

    # TODO: we'll eventually need to store geometry objects somewhere


class Verification(models.Model):
    report = models.ForeignKey(CSSCall)
    property_desciption = models.CharField(max_length=256, null=True, blank=True)
    owner_name = models.CharField(max_length=256, null=True, blank=True)
    owner_address = models.CharField(max_length=256, null=True, blank=True)
    owner_primary_contact = models.CharField(max_length=256, null=True, blank=True)
    owner_secondary_contact = models.CharField(max_length=256, null=True, blank=True)


class RecordingType(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)


class Recording(models.Model):
    recording_type = models.ForeignKey(RecordingType)
    call = models.ForeignKey(CSSCall)
    url = models.CharField(max_length=256, null=True, blank=True)


class CSSCaseAssignee(models.Model):
    case = models.ForeignKey(CSSCase, null=True, blank=True)
    assignee_name = models.CharField(max_length=256, null=True, blank=True)
