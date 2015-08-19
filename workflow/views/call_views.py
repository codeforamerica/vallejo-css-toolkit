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
from workflow.sql import AUDIT_LOG_DATA_SQL, CURRENT_USER_ASSIGNMENTS_SQL
from workflow.utils.call_utils import get_calls_data, create_call_audit_items

log = logging.getLogger('consolelogger')


@login_required
def call(request, call_id):
    instance = get_object_or_404(Call, id=call_id)
    form = CallForm(request.POST or None, instance=instance)

    if form.is_valid():
        call = form.save()
        user = get_object_or_404(User, id=request.user.id)
        create_call_audit_items(form.cleaned_data, form.initial, user, call)
        messages.add_message(request, messages.SUCCESS, 'Call successfully updated.')

        return HttpResponseRedirect('/workflow/call/%d' % call.id)

    return render(request, 'workflow/call.html', {'form': form})

@login_required
def audit_log_data(request):
    cursor = connection.cursor()
    try:
        cursor.execute(AUDIT_LOG_DATA_SQL)
        results = dictfetchall(cursor)
    except Exception as e:
        results = []
        log.error('Error encountered fetching from database: {}'.format(e))
        # messages.add()
    finally:
        cursor.close()

    return JsonResponse({'results': results})

@login_required
def audit_log(request):
    return render(request, 'workflow/audit_log.html')

@login_required
def calls_data(request):
    results = get_calls_data(dict(request.GET.items()))
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
