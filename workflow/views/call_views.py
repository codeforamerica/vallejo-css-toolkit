import logging
import traceback
from itertools import chain
from datetime import datetime

import usaddress

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from common.datatables import get_datatables_data

# from intake.models import Call
# from intake.forms import CallForm
# from intake.models import CallAuditItem, STATUS_CHOICES

from workflow.forms import CSSCallForm
from workflow.sql import CALLS_DATA_SQL, AUDIT_LOG_DATA_SQL
from workflow.models import CSSCall, PDCase, CRWCase, CSSCase

log = logging.getLogger('consolelogger')

CALLS_IDX_COLUMN_MAP = [
    'id',
    'reported_datetime',
    'reported_datetime_link',
    'caller_name',
    'caller_name_link'
    'caller_number',
    'caller_number_link',
    'problem_address',
    'problem_address_link',
    'status',
    'status_link',
    'resolution',
    'resolution_link',
    'count',
    'tcount'
]


@login_required(login_url='/admin/login/')
def add_call(request):
    form = CSSCallForm(request.POST or None, initial={'reported_datetime': datetime.now()})
    if form.is_valid():
        call = form.save()
        messages.add_message(request, messages.SUCCESS, 'Report successfully added.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(request, 'workflow/css_call.html', {'form': form})

@login_required(login_url='/admin/login/')
def call(request, call_id):
    instance = get_object_or_404(CSSCall, id=call_id)
    form = CSSCallForm(request.POST or None, instance=instance)

    pd_cases = []
    crw_cases = []
    css_cases = []

    # TODO, join this on the actual csscall address number and street name
    tagged = usaddress.tag(instance.address)
    if tagged and tagged[1] == 'Street Address':
        address_number = tagged[0].get('AddressNumber')
        street_name = tagged[0].get('StreetName')
        if address_number and address_number.isdigit() and street_name:
            pd_cases = PDCase.objects.filter(address_number=int(address_number), street_name=street_name.upper()).values_list('id', 'address_number', 'street_name')
            crw_cases = CRWCase.objects.filter(address_number=int(address_number), street_name=street_name.upper()).values_list('id', 'address_number', 'street_name')
            css_cases = CSSCase.objects.filter(address_number=int(address_number), street_name=street_name.upper()).values_list('id', 'address_number', 'street_name')

            pd_cases = [list(c) + ['RMS'] for c in pd_cases]
            crw_cases = [list(c) + ['CRW'] for c in crw_cases]

    # TODO, join this on the actual csscall address number and street name
    if instance.address:
        css_calls = CSSCall.objects.filter(address=instance.address).values_list('id', 'reported_datetime')
    else:
        css_calls = [(instance.id, instance.reported_datetime)]

    if form.errors:
        messages.add_message(request, messages.ERROR, form.errors)

    if form.is_valid():
        call = form.save()
        messages.add_message(request, messages.SUCCESS, 'Report successfully updated.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(
        request,
        'workflow/css_call.html',
        {
            'id': instance.id,
            'form': form,
            'css_cases': css_cases,
            'external_cases': list(chain(pd_cases, crw_cases)),
            'css_calls': css_calls
        }
    )

# @login_required(login_url='/admin/login/')
# def call(request, call_id):
#     instance = get_object_or_404(Call, id=call_id)
#     form = CallForm(request.POST or None, instance=instance)

#     if form.is_valid():
#         call = form.save()
#         user = get_object_or_404(User, id=request.user.id)
#         for field, new_value in form.cleaned_data.iteritems():
#             old_value = form.initial.get(field)

#             if field == 'assignee':
#                 if old_value:
#                     old_assignee = get_object_or_404(User, id=old_value)
#                     old_value = old_assignee.get_full_name()

#                 if new_value:    
#                     new_assignee = get_object_or_404(User, username=new_value)
#                     new_value = new_assignee.get_full_name()

#             if field == 'status':
#                 for status_choice in STATUS_CHOICES:
#                     if old_value == status_choice[0]:
#                         old_value = status_choice[1]
#                     if new_value == status_choice[0]:
#                         new_value = status_choice[1]

#             if (old_value or new_value) and old_value != new_value:
#                 CallAuditItem.objects.create(user=user, call=call, changed_field=field, old_value=old_value, new_value=new_value)

#         messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

#         return HttpResponseRedirect('/workflow/call/%d' % call.id)

#     return render(request, 'workflow/call.html', {'form': form})

@login_required(login_url='/admin/login/')
def call_audit_log_data(request):
    request_dict = dict(request.GET.items())
    idx_column_map = ['call_time', 'timestamp', 'name', 'changed_field', 'old_value', 'new_value', 'count', 'tcount']

    try:
        results = get_datatables_data(request_dict, AUDIT_LOG_DATA_SQL, idx_column_map)
    except Exception:        
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc().replace('\n', '\t')))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)

@login_required(login_url='/admin/login/')
def call_audit_log(request):
    return render(request, 'workflow/call_audit_log.html')

@login_required(login_url='/admin/login/')
def calls_data(request):
    request_dict = dict(request.GET.items())

    try:
        results = get_datatables_data(request_dict, CALLS_DATA_SQL, CALLS_IDX_COLUMN_MAP)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)

@login_required(login_url='/admin/login/')
def calls(request):
    return render(request, 'workflow/calls.html')
