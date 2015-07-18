from django.db import models

class Call(models.Model):
    call_sid = models.CharField(max_length=256, null=True)
    caller_name = models.CharField(max_length=256, null=True)
    name_recording_url = models.CharField(max_length=256, null=True)
    caller_number = models.BigIntegerField(null=True)
    call_time = models.DateTimeField(auto_now_add=True)
    caller_preferred_contact = models.IntegerField(null=True)
    problem_address = models.CharField(max_length=256, null=True)
    address_recording_url = models.CharField(max_length=256, null=True)
    problem_description = models.CharField(max_length=1024, null=True)
    description_recording_url = models.CharField(max_length=256, null=True)
