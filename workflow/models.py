from django.db import models

from geo.models import Address


class CaseStatus(models.Model):
    name = models.CharField(max_length=256)

class Case(models.Model):
    description = models.CharField(max_length=1024, null=True)
    status = models.ForeignKey(CaseStatus)
    resolution = models.CharField(max_length=1024, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)


# need util script to import rims data from other db, geocode the addresses, and create Case objects for them

# will need to parse the string since the address contains the street numnber with the steet name, then pass to geocode()
