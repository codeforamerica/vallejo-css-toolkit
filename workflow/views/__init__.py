import calendar
from datetime import datetime

import pytz

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect

from workflow.models import CSSCall, CSSCase


@login_required(login_url='/login/')
def landing(request):

    # TODO: do a proper filter
    newest_calls = CSSCall.objects.filter()[:5].values_list('date', 'name', 'address', 'problem', 'id')

    # TODO: fetch this from the case audit log when it's implemented
    recent_activities = [
        'Tina Encarnacion contacted the owner of 2 Florida Street.',
        'Lt. Park closed a case at 555 Santa Clara Street.',
        'Cpl. Garcia conducted a site visit at 111 Amador Street.'
    ]

    now = pytz.timezone('America/Los_Angeles').localize(datetime.now())
    start_of_month = datetime(now.year, now.month, 1, 0, 0, 0, tzinfo=now.tzinfo)
    if start_of_month.month == 1:
        start_of_last_month = datetime(start_of_month.year - 1, 12, 1, 0, 0, 0, tzinfo=start_of_month.tzinfo)
    else:
        start_of_last_month = datetime(start_of_month.year, start_of_month.month - 1, 1, 0, 0, 0, tzinfo=start_of_month.tzinfo)

    # one_month_ago = now - timedelta(month=1)
    _, days_in_month = calendar.monthrange(now.year, now.month)

    current_month_new_reports = CSSCall.objects.filter(reported_datetime__gte=start_of_month).count()
    last_month_new_reports = CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month).count()
    current_month_new_cases = CSSCase.objects.filter(created_at__gte=start_of_month).count()
    last_month_new_cases = CSSCase.objects.filter(created_at__gte=start_of_last_month, created_at__lt=start_of_month).count()

    return render(
        request,
        'workflow/landing.html',
        {
            # 'newest_calls': newest_calls,
            # 'recent_activities': recent_activities,
            # 'new_report_count': 17

            'current_month_new_reports': current_month_new_reports,
            'last_month_new_reports': last_month_new_reports,

            'current_month_new_cases': current_month_new_cases,
            'last_month_new_cases': last_month_new_cases,

        }
    )


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Successfully logged out.")
    return HttpResponseRedirect('/login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.WARNING, "This user account is disabled.")
        else:
            messages.add_message(request, messages.WARNING, "The user nane or password is incorrect.")
    else:
        users = User.objects.filter(id=request.user.id)
        user = users and users[0]
        if user and user.is_authenticated:
            return HttpResponseRedirect('/')

    return render(request, 'workflow/login.html', {'exclude_navbar': True})
