import traceback
import logging

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from intake.models import Call
from intake.forms import CallForm
from workflow.sql import CALLS_DATA_SQL
from common.datatables import get_datatables_data
from intake.models import CallAuditItem, STATUS_CHOICES
from workflow.sql import AUDIT_LOG_DATA_SQL

from workflow.models import CSSCall, PDCase, CRWCase, CSSCase
from workflow.forms import CSSCallForm

log = logging.getLogger('consolelogger')


@login_required(login_url='/admin/login/')
def add_call(request):
    form = CSSCallForm(request.POST or None)
    if form.is_valid():
        call = form.save()
        messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(request, 'workflow/css_call.html', {'form': form})

@login_required(login_url='/admin/login/')
def call(request, call_id):
    instance = get_object_or_404(CSSCall, id=call_id)
    form = CSSCallForm(request.POST or None, instance=instance)

    pd_cases = []
    crw_cases = []
    css_cases = []
    import usaddress
    tagged = usaddress.tag(instance.address)
    if tagged and tagged[1] == 'Street Address':
        address_number = tagged[0].get('AddressNumber')
        street_name = tagged[0].get('StreetName')
        if address_number and address_number.isdigit() and street_name:
            pd_cases = PDCase.objects.filter(address_number=int(address_number), street_name=street_name.upper())
            crw_cases = CRWCase.objects.filter(address_number=int(address_number), street_name=street_name.upper())
            css_cases = CSSCase.objects.filter(address_number=int(address_number), street_name=street_name.upper())

    if form.is_valid():
        call = form.save()
        messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(request, 'workflow/css_call.html', {'form': form, 'pd_cases': pd_cases, 'crw_cases': crw_cases, 'css_cases': css_cases})

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
    idx_column_map = ['id', 'call_time', 'caller_name', 'caller_number', 'problem_address', 'status', 'assignee', 'raw_id', 'count', 'tcount']

    try:
        results = get_datatables_data(request_dict, CALLS_DATA_SQL, idx_column_map)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)

@login_required(login_url='/admin/login/')
def calls(request):
    return render(request, 'workflow/calls.html')
