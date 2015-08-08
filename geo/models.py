from django.db import models

class Address(models.Model):
    street_number = models.IntegerField(null=True)
    street_name = models.CharField(max_length=256, null=True)
    street_descriptor = models.CharField(max_length=256, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
