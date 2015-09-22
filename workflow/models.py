from django.db import models
from django.contrib.auth.models import User

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
    assignee = models.ForeignKey(User, null=True, blank=True)

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
    assignee = models.ForeignKey(User, null=True, blank=True)
