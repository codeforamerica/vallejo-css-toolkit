import json
import logging
import traceback
from datetime import datetime

import pytz
import twilio.twiml

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_twilio.decorators import twilio_view

from intake.models import Call, TypeformSubmission, TypeformAsset
from workflow.models import CSSCall
from data_load.models import RMSCase

# from intake.utils import create_call, update_call

log = logging.getLogger('consolelogger')


@twilio_view
def step_one(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-two/", numDigits=1, method="POST") as g:
        g.say("Hello, you've reached the CSS-tool. Here you can report issues in your neighborhood or leave a question or message for the Community Services Section. If you are experiencing an emergency, please call 9 1 1. Press 1 if you're calling to report an issue, press 2 if you're calling to ask a question or leave a message.")

    return resp


@twilio_view
def step_two(request):
    digit_pressed = request.POST.get('Digits', None)

    resp = twilio.twiml.Response()

    if digit_pressed and digit_pressed.isdigit():
        if int(digit_pressed) == 2:
            resp.say("What is your message or question? When you are finished, press pound.")
            resp.record(
                action="/intake/step-nine/",
                finishOnKey="#",
                method="POST",
                timeout=30
            )

        else:
            resp.say("Where is the issue occurring? Please say the address or cross streets.")
            resp.record(
                action="/intake/step-three/",
                finishOnKey="#",
                method="POST",
                timeout=30
            )

    return resp


@twilio_view
def step_three(request):
    resp = twilio.twiml.Response()

    resp.say("Describe the issue you're calling about. When you are finished, press pound.")

    resp.record(
        action="/intake/step-four/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_four(request):
    resp = twilio.twiml.Response()

    resp.say("How long has this issue been occurring?")

    resp.record(
        action="/intake/step-five/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_five(request):
    resp = twilio.twiml.Response()

    resp.say("Around what time of day does this issue occur?")

    resp.record(
        action="/intake/step-six/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_six(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-seven/", numDigits=1, method="POST") as g:
        g.say("How many people are involved in this issue? Answer using a number on your keyboard. If you are unsure, press pound.")

    return resp


@twilio_view
def step_seven(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-eight/", numDigits=1, method="POST") as g:
        g.say("Are there safety concerns at this location that we should be aware of? If yes, press 1. If no, press 2. If you are unsure, press 3.")

    return resp


@twilio_view
def step_eight(request):
    resp = twilio.twiml.Response()

    resp.say("Have you ever reported this issue before? If so, when? If not, press pound.")

    resp.record(
        action="/intake/step-nine/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_nine(request):
    resp = twilio.twiml.Response()

    resp.say("It's helpful if we have your name and contact information in case we need any further details on how to best resolve this issue. We will never share your information with anyone other than authorized city staff.")
    resp.say("What is your name?")

    resp.record(
        action="/intake/step-ten/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_ten(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-eleven/", numDigits=10, method="POST") as g:
        g.say("What is your phone number, starting with the area code? Answer using the numbers on your keyboard.")

    return resp


@twilio_view
def step_eleven(request):
    resp = twilio.twiml.Response()

    resp.say("What is your email address?")

    resp.record(
        action="/intake/step-twelve/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_twelve(request):
    resp = twilio.twiml.Response()

    resp.say("What is your home address?")

    resp.record(
        action="/intake/step-thirteen/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )

    return resp


@twilio_view
def step_thirteen(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-fourteen/", numDigits=1, method="POST") as g:
        g.say("Where should we send you the receipt and progress updates for this report? Press 1 for email updates, press 2 for text message updates, press 3 if you would not like a receipt and progress updates.")

    return resp


@twilio_view
def step_fourteen(request):
    resp = twilio.twiml.Response()

    resp.say("Thank you, your report has been sent to the Community Services Section. Have a good day.")

    return resp


### Original intake view below ###

@twilio_view
def welcome(request):
    resp = twilio.twiml.Response()
    resp.say("Hello! Thank you for calling the Community Services Section of the Vallejo Police Department.")
    resp.pause(length=1)

    call_sid = request.POST.get('CallSid', None)
    Call.objects.create(call_sid=call_sid)

    resp.say("Please say your name, ending with the pound key.")
    resp.record(
        action="/intake/handle-name/",
        transcribe=True,
        transcribeCallback="/intake/handle-name-transcription/",
        finishOnKey="#",
        method="POST"
    )

    return resp


@twilio_view
def sms_reply(request):
    resp = twilio.twiml.Response()
    resp.message("Thank you for your message. We appreciate your input.")

    return resp


@twilio_view
def handle_name(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    name_recording_url = request.POST.get("RecordingUrl", None)
    call.name_recording_url = name_recording_url

    call.save()

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/handle-feedback-pref/", numDigits=1, method="POST") as g:
        g.say("Would you like to receive automated feedback about progress on this report? Press 1 for phone call, 2 for text. Press 3 if you wish not to receive updates.")

    return resp


@twilio_view
def handle_name_transcription(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    name_transcription = request.POST.get("TranscriptionText", None)
    call.caller_name = name_transcription

    call.save()

    return JsonResponse({'status': 'OK'})


@twilio_view
def handle_feedback_pref(request):
    digit_pressed = request.POST.get('Digits', None)

    resp = twilio.twiml.Response()

    if digit_pressed and digit_pressed.isdigit():
        call_sid = request.POST.get('CallSid', None)
        call = Call.objects.get(call_sid=call_sid)
        call.caller_preferred_contact = int(digit_pressed)
        call.save()

        # TODO: need to handle no contact preferred

        # if int(digit_pressed) in [1, 2]:
    with resp.gather(action="/intake/handle-feedback-number/", numDigits=10, method="POST") as g:
        g.say("Please enter your preferred phone number to receive updates, beginning with the area code.")

    return resp


@twilio_view
def handle_feedback_number(request):
    digits_pressed = request.POST.get('Digits', None)
    if digits_pressed and digits_pressed.isdigit() and len(digits_pressed) == 10:
        call_sid = request.POST.get('CallSid', None)
        call = Call.objects.get(call_sid=call_sid)

        call.caller_number = int(digits_pressed)
        call.save()

    resp = twilio.twiml.Response()

    resp.say("Please say the address you're calling to report, ending with the pound key.")
    resp.record(
        action="/intake/handle-problem-address/",
        transcribe=True,
        transcribeCallback="/intake/handle-problem-address-transcription/",
        finishOnKey="#",
        method="POST"
    )

    return resp


@twilio_view
def handle_problem_address(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    address_recording_url = request.POST.get("RecordingUrl", None)
    call.address_recording_url = address_recording_url

    call.save()

    resp = twilio.twiml.Response()

    resp.say("Please briefly describe the issue, ending with the pound key.")
    resp.record(
        action="/intake/handle-problem-description/",
        transcribe=True,
        transcribeCallback="/intake/handle-problem-description-transcription/",
        finishOnKey="#",
        timeout=30,
        method="POST"
    )

    return resp


@twilio_view
def handle_problem_address_transcription(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    address_transcription = request.POST.get("TranscriptionText", None)
    call.problem_address = address_transcription

    call.save()

    return JsonResponse({'status': 'OK'})


@twilio_view
def handle_problem_description(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    description_recording_url = request.POST.get("RecordingUrl", None)
    call.description_recording_url = description_recording_url

    call.save()

    resp = twilio.twiml.Response()
    resp.say("Thank you for reporting this issue. Goodbye.")

    return resp


@twilio_view
def handle_problem_description_transcription(request):
    call_sid = request.POST.get('CallSid', None)
    call = Call.objects.get(call_sid=call_sid)

    description_transcription = request.POST.get("TranscriptionText", None)
    call.problem_description = description_transcription

    call.save()

    return JsonResponse({'status': 'OK'})


@csrf_exempt
def handle_typeform(request):
    log.info(request.POST)

    try:

        TypeformSubmission.objects.create(typeform_json=json.dumps(request.POST))

        address = request.POST.get("Where is the problem occurring?")
        phone = request.POST.get("What is your phone number?")
        name = request.POST.get("What is your name?")
        problem = request.POST.get("Please describe what is happening.")
        reporter_street_name = request.POST.get("What is your home address?")
        problem_duration = request.POST.get("How long has the problem been occurring?")
        reporter_alternate_contact = request.POST.get("What is your email address?")
        reported_before = request.POST.get("Have you ever reported this problem before?")
        if reported_before != "0":
            when_last_reported = request.POST.get("When did you last report this problem?")
        else:
            when_last_reported = None
        time_of_day_occurs = request.POST.get("What time of day does the problem occur?")

        num_people_involved = request.POST.get("How many people are involved?")
        safety_concerns = request.POST.get("Are there safety concerns at the location you are reporting?")

        utc = pytz.utc
        reported_datetime = utc.localize(datetime.utcnow())

        asset_url = request.POST.get("Do you have photos of the problem?")

        c = CSSCall.objects.create(
            address=address,
            phone=phone,
            name=name,
            problem=problem,
            reporter_street_name=reporter_street_name,
            problem_duration=problem_duration,
            reporter_alternate_contact=reporter_alternate_contact,
            when_last_reported=when_last_reported,
            time_of_day_occurs=time_of_day_occurs,
            num_people_involved=num_people_involved,
            safety_concerns=safety_concerns,
            reported_datetime=reported_datetime
        )

        if asset_url:
            TypeformAsset.objects.create(
                css_report=c,
                asset_url=asset_url
            )

    except Exception:
        log.error(traceback.format_exc())

    return JsonResponse({'status': 'OK'})


@csrf_exempt
def get_latest_case_no(request):
    log.info(request.POST)
    log.info('fetching latest rms case num')

    result = list(RMSCase.objects.raw("SELECT id, case_no FROM data_load_rmscase ORDER BY case_no DESC LIMIT 1"))

    if result:
        latest_case_no = result[0].case_no

    else:
        latest_case_no = 0

    return JsonResponse({'latest_case_no': latest_case_no})


@csrf_exempt
def handle_rms_post(request):
    log.info('hanlding update from rms')

    cases = json.loads(request.body)
    tz = pytz.timezone('America/Los_Angeles')

    for case in cases:
        date = case[1]
        date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

        rms_case = RMSCase.objects.get_or_create(case_no=case[0])
        rms_case.date = date_converted
        rms_case.code = case[2]
        rms_case.desc = case[3]
        rms_case.incnum = case[4]
        rms_case.address = case[5]
        rms_case.off_name = case[7]
        rms_case.save()

    return JsonResponse({'status': 'OK'})


@csrf_exempt
def handle_crw_post(request):
    log.info(request.POST)
    log.info('hanlding update from crw')

#   CASE_NO, CASE_NAME, STARTED, STARTED_BY, CLOSED, CLOSED_BY, LASTACTION, CaseType, CaseSubType,
#    SITE_NUMBER, SITE_STREETNAME, ASSIGNED_TO, STATUS

    return JsonResponse({'status': 'OK'})
