from django.db import models


class CaseStatus(models.Model):
    name = models.CharField(max_length=256)

class CSSCase(models.Model):
    description = models.CharField(max_length=1024, null=True)
    resolution = models.CharField(max_length=1024, null=True)
    status = models.ForeignKey(CaseStatus, null=True)
    address_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)

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
    problem = models.CharField(max_length=256, null=True, blank=True)
    date = models.CharField(max_length=256, null=True, blank=True)
    resolution = models.CharField(max_length=256, null=True, blank=True)
