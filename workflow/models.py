from django.db import models

# from geo.utils.geocode import geocode
# from geo.utils.normalize_address import normalize_address_string

class CaseStatus(models.Model):
    name = models.CharField(max_length=256)

# class CaseLocation(models.Model):
#     street_number = models.IntegerField(null=True)
#     street_name = models.CharField(max_length=256, null=True)
#     street_descriptor = models.CharField(max_length=256, null=True)

    # def geocode(self):
    #     if self.street_number and self.street_name:
    #         return geocode(self.street_number, self.street_name, street_descriptor=self.street_descriptor)

class CSSCase(models.Model):
    description = models.CharField(max_length=1024, null=True)
    resolution = models.CharField(max_length=1024, null=True)
    status = models.ForeignKey(CaseStatus, null=True)
    raw_address = models.CharField(max_length=256, null=True)
    # case_location = models.ForeignKey(CaseLocation, null=True)

    # def geocode(self):
    #     if self.raw_address:
    #         normalized = normalize_address_string(self.raw_address)
    #         if normalized:
    #             street_number, street_name, street_descriptor = normalized
    #             return geocode(street_number, street_name, street_descriptor)

class PDCase(models.Model):
    raw_address = models.CharField(max_length=256, null=True)
    # case_location = models.ForeignKey(CaseLocation, null=True)
