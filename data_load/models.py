from django.db import models


class RMSCase(models.Model):
    case_no = models.BigIntegerField()
    date = models.DateTimeField(null=True)
    code = models.CharField(max_length=1024, null=True)
    desc = models.CharField(max_length=1024, null=True)
    incnum = models.BigIntegerField(null=True)
    address = models.CharField(max_length=1024, null=True)
    off_name = models.CharField(max_length=1024, null=True)


class CRWCase(models.Model):
    yr_no = models.IntegerField()
    seq_no = models.IntegerField()
    case_no = models.CharField(max_length=1024, null=True)
    started = models.DateTimeField(null=True)
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=1024, null=True)
    assigned_to = models.CharField(max_length=1024, null=True)
    status = models.CharField(max_length=1024, null=True)
    desc = models.CharField(max_length=1024, null=True)
    case_type = models.CharField(max_length=1024, null=True)
    case_subtype = models.CharField(max_length=1024, null=True)


class RMSInciden(models.Model):
    incident_no = models.BigIntegerField()
