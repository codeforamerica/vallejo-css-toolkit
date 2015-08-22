import traceback
import logging

from django.db import connection
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from intake.models import Call
from intake.forms import CallForm
from common.utils import dictfetchall
from workflow.sql import CALLS_DATA_SQL
from common.datatables import get_datatables_data
from intake.models import CallAuditItem, STATUS_CHOICES
from workflow.sql import AUDIT_LOG_DATA_SQL, CURRENT_USER_ASSIGNMENTS_SQL

log = logging.getLogger('consolelogger')


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

        messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(request, 'workflow/call.html', {'form': form})

@login_required
def call_audit_log_data(request):
    request_dict = dict(request.GET.items())
    idx_column_map = ['call_time', 'timestamp', 'name', 'changed_field', 'old_value', 'new_value', 'count', 'tcount']

    try:
        results = get_datatables_data(request_dict, AUDIT_LOG_DATA_SQL, idx_column_map)
    except Exception as e:        
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc().replace('\n', '\t')))
        results = {'data': [], 'filteredRecords': 0, 'totalRecords': 0}

    return JsonResponse(results)

@login_required
def call_audit_log(request):
    return render(request, 'workflow/call_audit_log.html')

@login_required
def calls_data(request):
    request_dict = dict(request.GET.items())
    idx_column_map = ['call_time', 'caller_name', 'caller_number', 'problem_address', 'status', 'assignee', 'count', 'tcount']

    try:
        results = get_datatables_data(request_dict, CALLS_DATA_SQL, idx_column_map)
    except Exception as e:        
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc().replace('\n', '\t')))
        results = {'data': [], 'filteredRecords': 0, 'totalRecords': 0}

    return JsonResponse(results)

@login_required
def calls(request):
    return render(request, 'workflow/calls.html')

@login_required
def assigned_to_current_user_data(request):
    current_user = get_object_or_404(User, id=request.user.id)
    cursor = connection.cursor()

    try:
        cursor.execute(CURRENT_USER_ASSIGNMENTS_SQL, [current_user.id])
        results = dictfetchall(cursor)
    except Exception as e:
        results = []
        log.error('Error encountered fetching from database: {}'.format(e))
        # messages.add()
    finally:
        cursor.close()

    return JsonResponse({'results': results})

@login_required
def assigned_to_current_user(request):
    return render(request, 'workflow/my_assignments.html')
