import re
import json

import twilio.twiml
from psycopg2.extensions import AsIs

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
from intake.sql import AUDIT_LOG_DATA_SQL, CURRENT_USER_ASSIGNMENTS_SQL, CALLS_DATA_SQL, TOTAL_CALLS_COUNT_SQL


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
    cursor.execute(AUDIT_LOG_DATA_SQL)
    
    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def audit_log(request):

    return render(request, 'intake/audit_log.html')

@login_required
def assigned_to_current_user_data(request):

    current_user = get_object_or_404(User, id=request.user.id)

    cursor = connection.cursor()
    cursor.execute(CURRENT_USER_ASSIGNMENTS_SQL, [current_user.id])
    
    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def assigned_to_current_user(request):

    return render(request, 'intake/my_assignments.html')

@login_required
def calls_data(request):
    idx_column_map = ['call_time', 'caller_name', 'caller_number', 'problem_address', 'status', 'assignee', 'count']

    searchable_columns = []
    search = None
    offset = 0
    limit = 10
    sort_by = 1
    sort_dir = 'asc'

    for k, v in request.GET.iteritems():
        if k == 'start' and v.isdigit():
            offset = int(v)

        if k == 'length' and v.isdigit():
            limit = int(v)

        if k == 'order[0][column]' and v.isdigit():
            sort_by = int(v) + 1  # psql column indicies start at 1

        if k == 'order[0][dir]' and v in ('asc', 'desc'):
            sort_dir = v

        if k == 'search[value]':
            search = v

        r = re.match('columns\[(?P<idx>\d+)\]\[searchable\]', k)
        if r and v == 'true':
            searchable_idx = r.groupdict()['idx']
            searchable_columns.append(idx_column_map[int(searchable_idx)])

    search_string = ''
    if search:
        search_cols_modified = [" {} ilike '%{}%' ".format(searchable_column, search) for searchable_column in searchable_columns]
        search_string = "WHERE {}".format(' OR '.join(search_cols_modified))

    cursor = connection.cursor()
    cursor.execute(CALLS_DATA_SQL, [AsIs(search_string), sort_by, AsIs(sort_dir), offset, limit])
    
    data_results = cursor.fetchall()
    if data_results:
        records_filtered = data_results[0][-1]
    else:
        records_filtered = 0

    cursor.execute(TOTAL_CALLS_COUNT_SQL)
    count_results = dictfetchall(cursor)
    if count_results:
        records_total = count_results[0].get('records_total', 0)
    else:
        records_total = 0

    return JsonResponse({'data': data_results, 'recordsTotal': records_total, 'recordsFiltered': records_filtered})

@login_required
def calls(request):

    return render(request, 'intake/calls.html')
