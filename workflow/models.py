from django.db import models

from geo.models import Address


class CaseStatus(models.Model):
    name = models.CharField(max_length=256)

# dept -> 1 = PD
class Case(models.Model):
    description = models.CharField(max_length=1024, null=True)
    status = models.ForeignKey(CaseStatus)
    resolution = models.CharField(max_length=1024, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    dept = models.IntegerField(null=True)
