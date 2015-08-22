from django.db import models


class CaseStatus(models.Model):
    name = models.CharField(max_length=256)

class CSSCase(models.Model):
    description = models.CharField(max_length=1024, null=True)
    resolution = models.CharField(max_length=1024, null=True)
    status = models.ForeignKey(CaseStatus, null=True)
    raw_address = models.CharField(max_length=256, null=True)

class PDCase(models.Model):
    raw_address = models.CharField(max_length=256, null=True)
