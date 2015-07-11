import twilio.twiml
from django_twilio.decorators import twilio_view

@twilio_view
def welcome(request):
    resp = twilio.twiml.Response()
    resp.say("Hello! Thank you for calling.")

    return resp
