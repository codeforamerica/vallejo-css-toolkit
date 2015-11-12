import os
import json
import logging
import traceback
import tempfile
from datetime import datetime

import boto
import pytz
import twilio.twiml
from boto.s3.key import Key

from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django_twilio.decorators import twilio_view

from intake.models import Call, TypeformSubmission, TypeformAsset, PublicUploadedAsset
from workflow.models import CSSCall, Recording
from intake.forms import IntakeIssueForm, IntakeContactForm

# from intake.utils import create_call, update_call

log = logging.getLogger('consolelogger')

SUPPORTED_LANGS = ('en')
DEFAULT_LANG = 'en'


def report_intro(request):
    lang = request.GET.get('lang') and request.GET['lang'] in SUPPORTED_LANGS or DEFAULT_LANG

    return render(request, 'intake/intake_intro.html', {'lang': lang, 'exclude_navbar': True})


def report_issue(request):
    if request.method == 'POST':
        form = IntakeIssueForm(request.POST, request.FILES)
        lang = form.data.get('lang', DEFAULT_LANG)

        if form.is_valid():
            now_utc = pytz.UTC.localize(datetime.utcnow())

            report = CSSCall.objects.create(
                address=form.cleaned_data.get('problem_location'),
                problem=form.cleaned_data.get('description'),
                num_people_involved=form.cleaned_data.get('how_many_people'),
                safety_concerns=form.cleaned_data.get('safety_concerns'),
                reported_datetime=now_utc,
                time_of_day_occurs=form.cleaned_data.get('time_of_day'),
                problem_duration=form.cleaned_data.get('how_long'),
                when_last_reported=form.cleaned_data.get('reported_before_details'),
                source=CSSCall.WEB_SOURCE
            )

            try:
                conn = boto.connect_s3()
                b = conn.get_bucket('vallejo-css-toolkit')

                if form.files.get('uploaded_photo'):
                    tmpfile = tempfile.NamedTemporaryFile(delete=False)
                    for chunk in form.files['uploaded_photo'].chunks():
                        tmpfile.write(chunk)
                    tmpfile.close()

                    env = os.environ.get('DJANGO_SETTINGS_MODULE', 'not_set')

                    k = Key(b)
                    k.key = 'submitted-images/{}/{}/{}'.format(
                        env.split('.')[-1],
                        report.id,
                        tmpfile.name.split('/')[-1]
                    )
                    k.set_contents_from_filename(tmpfile.name)
                    PublicUploadedAsset.objects.create(css_report=report, fpath=k.key)

            except:
                log.error("Encountered exception attempting to upload submitted file: {}".format(traceback.format_exc()))

            return HttpResponseRedirect(
                '/report/contact/?report_id={}{}'.format(
                    report.id,
                    lang != DEFAULT_LANG and "&lang={}".format(lang) or ""
                )
            )

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors)

    else:
        lang = request.GET.get('lang') and request.GET['lang'] in SUPPORTED_LANGS or DEFAULT_LANG
        form = IntakeIssueForm()

    return render(request, 'intake/intake_issue.html', {'form': form, 'lang': lang, 'exclude_navbar': True})


def report_contact(request):
    if request.method == 'POST':
        form = IntakeContactForm(request.POST, request.FILES)
        lang = form.data.get('lang', DEFAULT_LANG)
        report_id = form.data.get('report_id')
        report = get_object_or_404(CSSCall, id=report_id)

        if form.is_valid():

            # TODO: update the report with contact data
            report.caller_preferred_contact = form.cleaned_data.get('reporter_contact_method')
            report.name = form.cleaned_data.get('reporter_name')
            report.reporter_street_name = form.cleaned_data.get('reporter_address')
            report.phone = form.cleaned_data.get('reporter_phone')
            report.reporter_alternate_contact = form.cleaned_data.get('reporter_email')

            report.save()

            return HttpResponseRedirect(
                '/report/finish/?report_id={}{}'.format(
                    report.id,
                    lang != DEFAULT_LANG and "&lang={}".format(lang) or ""
                )
            )

        if form.errors:
            messages.add_message(request, messages.ERROR, "Please resolve the error(s) listed below.")

    else:
        report_id = request.GET.get('report_id')
        report = get_object_or_404(CSSCall, id=report_id)
        lang = request.GET.get('lang') and request.GET['lang'] in SUPPORTED_LANGS or DEFAULT_LANG
        form = IntakeContactForm()

    return render(request, 'intake/intake_contact.html', {'form': form, 'lang': lang, 'report_id': report.id, 'exclude_navbar': True})


def report_finish(request):
    report_id = request.GET.get('report_id')
    lang = request.GET.get('lang') and request.GET['lang'] in SUPPORTED_LANGS or DEFAULT_LANG

    return render(request, 'intake/intake_finish.html', {'report_id': report_id, 'lang': lang, 'exclude_navbar': True})


@twilio_view
def step_one(request):
    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-two/", numDigits=1, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/intro.mp3")
    resp.redirect("/intake/step-one/", method="POST")

    return resp


@twilio_view
def step_two(request):
    digit_pressed = request.POST.get('Digits', None)
    call_sid = request.POST.get('CallSid', None)
    CSSCall.objects.create(call_sid=call_sid)

    resp = twilio.twiml.Response()

    if digit_pressed and digit_pressed.isdigit():
        if int(digit_pressed) == 2:
            resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_is_your_message.mp3")
            resp.record(
                action="/intake/step-nine/",
                finishOnKey="#",
                method="POST",
                timeout=30
            )
            resp.redirect("/intake/step-nine", method="POST")

        else:
            resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/where.mp3")
            resp.record(
                action="/intake/step-three/",
                finishOnKey="#",
                method="POST",
                timeout=30
            )
            resp.redirect("/intake/step-three/", method="POST")

    resp.redirect("/intake/step-two/")

    return resp


@twilio_view
def step_three(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    location_url = request.POST.get("RecordingUrl", None)
    if location_url:
        Recording.objects.create(call=call, url=location_url, type=Recording.LOCATION)

    resp = twilio.twiml.Response()
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/describe.mp3")

    resp.record(
        action="/intake/step-four/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-four/", method="POST")

    return resp


@twilio_view
def step_four(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    description_url = request.POST.get("RecordingUrl", None)
    if description_url:
        Recording.objects.create(call=call, url=description_url, type=Recording.DESCRIPTION)

    resp = twilio.twiml.Response()
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/how_long.mp3")

    resp.record(
        action="/intake/step-five/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-five/", method="POST")

    return resp


@twilio_view
def step_five(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    duration_url = request.POST.get("RecordingUrl", None)
    if duration_url:
        Recording.objects.create(call=call, url=duration_url, type=Recording.DURATION)

    resp = twilio.twiml.Response()
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_time_of_day.mp3")

    resp.record(
        action="/intake/step-six/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-six/", method="POST")

    return resp


@twilio_view
def step_six(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    time_of_day_url = request.POST.get("RecordingUrl", None)
    if time_of_day_url:
        Recording.objects.create(call=call, url=time_of_day_url, type=Recording.TIME_OF_DAY)

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-seven/", numDigits=1, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/how_many_use_keypad.mp3")
    resp.redirect("/intake/step-seven/", method="POST")

    return resp


@twilio_view
def step_seven(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    digit_pressed = request.POST.get('Digits', None)
    call.num_people_involved = digit_pressed
    call.save()

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-eight/", numDigits=1, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/are_there_safety_concerns.mp3")
    resp.redirect("/intake/step-eight/", method="POST")

    return resp


@twilio_view
def step_eight(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    digit_pressed = request.POST.get('Digits', None)
    if digit_pressed == '1':
        call.safety_concerns = 'Yes'
        call.save()

    elif digit_pressed == '2':
        call.safety_concerns = 'No'
        call.save()

    elif digit_pressed == '3':
        call.safety_concerns = 'Unsure'
        call.save()

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-nine/", numDigits=1, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/have_you_reported_this_before.mp3")
    resp.redirect("/intake/step-nine/", method="POST")

    return resp


@twilio_view
def step_nine(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    digit_pressed = request.POST.get('Digits', None)
    if digit_pressed == '1':
        call.reported_before = 'Yes'
        call.save()

    elif digit_pressed == '2':
        call.reported_before = 'No'
        call.save()

    elif digit_pressed == '3':
        call.reported_before = 'Unsure'
        call.save()

    resp = twilio.twiml.Response()
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/helpful_to_have_your_info.mp3")
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_is_your_name.mp3")

    resp.record(
        action="/intake/step-ten/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-ten/", method="POST")

    return resp


@twilio_view
def step_ten(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    name_url = request.POST.get("RecordingUrl", None)
    if name_url:
        Recording.objects.create(call=call, url=name_url, type=Recording.NAME)

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-eleven/", numDigits=10, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_is_your_phone_number.mp3")
    resp.redirect("/intake/step-eleven/", method="POST")

    return resp


@twilio_view
def step_eleven(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    digits_pressed = request.POST.get('Digits', None)
    call.phone = digits_pressed
    call.save()

    resp = twilio.twiml.Response()

    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_is_your_email_address.mp3")

    resp.record(
        action="/intake/step-twelve/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-twelve/", method="POST")

    return resp


@twilio_view
def step_twelve(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    email_url = request.POST.get("RecordingUrl", None)
    if email_url:
        Recording.objects.create(call=call, url=email_url, type=Recording.EMAIL)

    resp = twilio.twiml.Response()

    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_is_your_home_address.mp3")

    resp.record(
        action="/intake/step-thirteen/",
        finishOnKey="#",
        method="POST",
        timeout=30
    )
    resp.redirect("/intake/step-thirteen/", method="POST")

    return resp


@twilio_view
def step_thirteen(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    address_url = request.POST.get("RecordingUrl", None)
    if address_url:
        Recording.objects.create(call=call, url=address_url, type=Recording.ADDRESS)

    resp = twilio.twiml.Response()

    with resp.gather(action="/intake/step-fourteen/", numDigits=1, method="POST") as g:
        g.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/what_type_of_receipt_.mp3")
    resp.redirect("/intake/step-fourteen/", method="POST")

    return resp


@twilio_view
def step_fourteen(request):
    call_sid = request.POST.get('CallSid', None)
    call = CSSCall.objects.get(call_sid=call_sid)

    digit_pressed = request.POST.get('Digits', None)

    if digit_pressed == '1':
        call.caller_preferred_contact = CSSCall.EMAIL_CONTACT_PREFERENCE
        call.save()

    elif digit_pressed == '2':
        call.caller_preferred_contact = CSSCall.TEXT_CONTACT_PREFERENCE
        call.save()

    elif digit_pressed == '3':
        call.caller_preferred_contact = CSSCall.NO_CONTACT_PREFERENCE
        call.save()

    resp = twilio.twiml.Response()
    resp.play("https://s3.amazonaws.com/vallejo-css-toolkit/intake_files/thank_you.mp3")

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
