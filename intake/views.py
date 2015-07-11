import twilio.twiml

from django_twilio.decorators import twilio_view

from django.shortcuts import render
from django.http import HttpResponse

import twilio.twiml


@twilio_view
def welcome(request):
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello! Thank you for calling.")

    # return HttpResponse('<html><p>Success!</p></html>')

    return resp

# name, address, problem address

