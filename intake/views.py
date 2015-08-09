import json

import twilio.twiml

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.contrib.auth.decorators import login_required

from django_twilio.decorators import twilio_view

from intake.models import Call, CallAuditItem, STATUS_CHOICES
from intake.forms import CallForm
from intake.utils import create_call, update_call


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@twilio_view
def welcome(request):
    resp = twilio.twiml.Response()
    resp.say("Hello! Thank you for calling the Community Services Section of the Vallejo Police Department.")
    resp.pause(length=1)

    call_sid = request.POST.get('CallSid', None)
    call_id = Call.objects.create(call_sid=call_sid)

    resp.say("Please say your name, ending with the pound key.")
    resp.record(action="/intake/handle-name/", transcribe=True, transcribeCallback="/intake/handle-name-transcription/", finishOnKey="#", method="POST")

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
    resp.record(action="/intake/handle-problem-address/", transcribe=True, transcribeCallback="/intake/handle-problem-address-transcription/", finishOnKey="#", method="POST")

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
    resp.record(action="/intake/handle-problem-description/", transcribe=True, transcribeCallback="/intake/handle-problem-description-transcription/", finishOnKey="#", timeout=30, method="POST")

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

@login_required
def call(request, call_id):
    instance = get_object_or_404(Call, id=call_id)

    form = CallForm(request.POST or None, instance=instance)

    if form.is_valid():

        call = form.save()
        user = get_object_or_404(User, id=request.user.id)

        for field, new_value in form.cleaned_data.iteritems():
            old_value = form.initial.get(field)

            if field == 'assignee':
                if old_value:
                    old_assignee = get_object_or_404(User, id=old_value)
                    old_value = old_assignee.get_full_name()

                if new_value:    
                    new_assignee = get_object_or_404(User, username=new_value)
                    new_value = new_assignee.get_full_name()

            if field == 'status':
                for status_choice in STATUS_CHOICES:
                    if old_value == status_choice[0]:
                        old_value = status_choice[1]
                    if new_value == status_choice[0]:
                        new_value = status_choice[1]

            if (old_value or new_value) and old_value != new_value:
                CallAuditItem.objects.create(user=user, call=call, changed_field=field, old_value=old_value, new_value=new_value)

        from django.contrib import messages
        messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

        return HttpResponseRedirect('/intake/call/%d' % call.id)

    return render(request, 'intake/call.html', {'form': form})

@login_required
def audit_log_data(request):
    cursor = connection.cursor()
    cursor.execute(
        """
        set time zone 'America/Los_Angeles';

        select
            COALESCE(u.first_name, '') as first_name,
            COALESCE(u.last_name, '') as last_name,
            c.id,
            c.caller_number as caller_number,
            COALESCE(to_char(cai.timestamp, 'MM-DD-YYYY HH24:MI:SS'), '') as timestamp,
            replace(COALESCE(cai.changed_field, ''), '_', ' ') as changed_field,
            COALESCE(cai.old_value, '') as old_value,
            COALESCE(cai.new_value, '') as new_value
        from intake_call c
        join intake_callaudititem cai
            on c.id = cai.call_id
        left join auth_user u
            on cai.user_id = u.id
        order by timestamp desc;
        """
    )
    
    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def audit_log(request):

    return render(request, 'intake/audit_log.html')

@login_required
def assigned_to_current_user(request):

    current_user = get_object_or_404(User, id=request.user.id)

    cursor = connection.cursor()
    cursor.execute(
        """
        set time zone 'America/Los_Angeles';

        select a.caller_number,
        a.id,
        a.call_time,
        a.caller_name,
        a.problem_address,
        a.status,
        b.last_updated

        from

        (select
            c.id,
            c.caller_number as caller_number,
            COALESCE(to_char(c.call_time, 'MM-DD-YYYY HH24:MI:SS'), '') as call_time,
            COALESCE(c.caller_name, '') as caller_name,
            COALESCE(c.problem_address, '') as problem_address,
            c.status as status
        from
            intake_call c
        where
            assignee_id = %s
        order by
            c.call_time desc
        ) a

        left join

        (select
            COALESCE(to_char(max(cai.timestamp), 'MM-DD-YYYY HH24:MI:SS'), '') as last_updated,
            cai.call_id as call_id
        from
            intake_callaudititem cai
        group by
            cai.call_id
        ) as b

        on a.id = b.call_id
        ;
        """,
        [current_user.id]
    )
    
    results = dictfetchall(cursor)

    return render(request, 'intake/my_assignments.html', {'objs': json.dumps(results)})
