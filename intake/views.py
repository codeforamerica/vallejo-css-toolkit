import twilio.twiml
from django_twilio.decorators import twilio_view

from intake.models import Call

@twilio_view
def welcome(request):
    resp = twilio.twiml.Response()
    resp.say("Hello! Thank you for calling the Community Services Section of the Vallejo Police Department.")
    resp.pause(length=1)

    call_sid = request.POST.get('CallSid', None)
    call_id = Call.objects.create(call_sid=call_sid)

    resp.say("Please say your name.")
    resp.record(action="/intake/handle-name/", transcribe="true", method="POST")

    return resp

@twilio_view
def handle_name(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    name_recording_url = request.POST.get("RecordingUrl", None)
    call.name_recording_url = name_recording_url

    name_transcription = request.POST.get("TranscriptionText", None)
    call.caller_name = name_transcription

    call.save()

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/handle-feedback-pref/", numDigits=1, method="POST") as g:
        g.say("Would you like to receive automated feedback about progress on this report? Press 1 for phone call, 2 for text, or 3 for none.")

    return resp

@twilio_view
def handle_feedback_pref(request):
    digit_pressed = request.POST.get('Digits', None)

    resp = twilio.twiml.Response()

    if digit_pressed and digit_pressed.is_digit():
        call_sid = request.POST.get('CallSid', None)
        call = Call.objects.get(call_sid=call_sid)
        call.caller_preferred_contact = int(digit_pressed)
        call.save()

        # TODO: need to handle no contact preferred

        # if int(digit_pressed) in [1, 2]:
    with resp.gather(action="/intake/handle-feedback-number/", numDigits=10, method="POST") as g:
        g.say("Please enter your preferred phone number to receieve updates, beginning with the area code.")

    return resp

@twilio_view
def handle_feedback_number(request):
    digit_pressed = request.POST.get('Digits', None)
    if digit_pressed and digit_pressed.is_digit() and len(digit_pressed) == 10:
        call_sid = request.POST.get('CallSid', None)
        call = Call.objects.get(call_sid=call_sid)

        call.caller_number = int(digit_pressed)
        call.save()

    resp = twilio.twiml.Response()

    resp.say("Please say the address you're calling to report issues about.")
    resp.record(action="/intake/handle-problem-address/", transcribe="true", method="POST")

    return resp

@twilio_view
def handle_problem_address(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    address_recording_url = request.POST.get("RecordingUrl", None)
    call.address_recording_url = address_recording_url

    address_transcription = request.POST.get("TranscriptionText", None)
    call.problem_address = address_transcription

    call.save()

    resp = twilio.twiml.Response()

    resp.say("Please briefly describe the issue.")
    resp.record(action="/intake/handle-problem-description/", transcribe="true", timeout=30, method="POST")

    return resp

@twilio_view
def handle_problem_description(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    description_recording_url = request.POST.get("RecordingUrl", None)
    call.description_recording_url = description_recording_url

    description_recording_url = request.POST.get("RecordingUrl", None)
    call.description_recording_url = description_recording_url

    call.save()

    resp = twilio.twiml.Response()
    resp.say("Thank you for reporting this issue. Goodbye.")

    return resp