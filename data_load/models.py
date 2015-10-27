from django.db import models


class RMSCase(models.Model):
    case_no = models.BigIntegerField()
    date = models.DateTimeField(null=True)
    code = models.CharField(max_length=1024, null=True)
    desc = models.CharField(max_length=1024, null=True)
    incnum = models.BigIntegerField(null=True)
    address = models.CharField(max_length=1024, null=True)
    off_name = models.CharField(max_length=1024, null=True)
