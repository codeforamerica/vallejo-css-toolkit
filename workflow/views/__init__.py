import json
# import calendar
from datetime import datetime, timedelta

import pytz

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count

from workflow.models import CSSCall, CSSCase, StaffReportNotification, CaseAction, Verification


@login_required(login_url='/login/')
def landing(request):

    now = pytz.timezone('America/Los_Angeles').localize(datetime.now())
    start_of_month = datetime(now.year, now.month, 1, 0, 0, 0, tzinfo=now.tzinfo)
    two_weeks_ago = now - timedelta(days=14)
    two_days_ago = now - timedelta(seconds=2 * 24 * 60 * 60)
    if start_of_month.month == 1:
        start_of_last_month = datetime(start_of_month.year - 1, 12, 1, 0, 0, 0, tzinfo=start_of_month.tzinfo)
    else:
        start_of_last_month = datetime(start_of_month.year, start_of_month.month - 1, 1, 0, 0, 0, tzinfo=start_of_month.tzinfo)

    # _, days_in_month = calendar.monthrange(now.year, now.month)

    current_month_new_reports = CSSCall.objects.filter(reported_datetime__gte=start_of_month).count()
    last_month_new_reports = CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month).count()
    current_month_new_cases = CSSCase.objects.filter(created_at__gte=start_of_month).count()
    last_month_new_cases = CSSCase.objects.filter(created_at__gte=start_of_last_month, created_at__lt=start_of_month).count()

    resolved_cases_this_month = CSSCase.objects.filter(resolved_at__gte=start_of_last_month).count()
    resolved_cases_last_month = CSSCase.objects.filter(resolved_at__gte=start_of_last_month, resolved_at__lt=start_of_month).count()

    case_verification_ids_right_now = set(CSSCase.objects.all().values_list('verification_id', flat=True))
    verifications_ids_created_this_month = set(Verification.objects.filter(created_at__gte=start_of_month).values_list('id', flat=True))
    verifications_in_progress_this_month = len(verifications_ids_created_this_month - case_verification_ids_right_now)

    case_verification_ids_last_month = set(CSSCase.objects.filter(created_at__lt=start_of_month).values_list('verification_id', flat=True))
    verifications_ids_created_last_month = set(Verification.objects.filter(created_at__gte=start_of_last_month, created_at__lt=start_of_month).values_list('id', flat=True))
    verifications_in_progress_last_month = len(verifications_ids_created_last_month - case_verification_ids_last_month)

    case_actions = CaseAction.objects.filter(timestamp__gte=two_days_ago).order_by('-timestamp')
    recent_reports = CSSCall.objects.filter(reported_datetime__gte=two_days_ago).order_by('-reported_datetime')

    reports_by_source_this_month = sorted(CSSCall.objects.filter(reported_datetime__gte=start_of_month).values('source').annotate(dcount=Count('source')), key=lambda k: k['dcount'], reverse=True)
    reports_by_source_last_month = sorted(CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month).values('source').annotate(dcount=Count('source')), key=lambda k: k['dcount'], reverse=True)

    reports_by_source = []
    for report_data in reports_by_source_this_month:
        if report_data['source'] is not None:
            reports_by_source.append((
                report_data['source'],
                [i[1] for i in CSSCall.SOURCE_CHOICES if report_data['source'] == i[0]][0],
                report_data['dcount'],
                [i['dcount'] for i in reports_by_source_last_month if i['source'] == report_data['source']] and [i['dcount'] for i in reports_by_source_last_month if i['source'] == report_data['source']] or 0
            ))

    for report_data in reports_by_source_last_month:
        if report_data['source'] is not None:
            if report_data['source'] not in [i[0] for i in reports_by_source]:
                reports_by_source.append((
                    report_data['source'],
                    [i[1] for i in CSSCall.SOURCE_CHOICES if report_data['source'] == i[0]][0],
                    0,
                    report_data['dcount']
                ))

    reports_by_source.append((
        -1,
        'Unknown',
        CSSCall.objects.filter(reported_datetime__gte=start_of_month, source__isnull=True).count(),
        CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month, source__isnull=True).count()
    ))

    reports_by_report_type_this_month = sorted(CSSCall.objects.filter(reported_datetime__gte=start_of_month).values('report_type').annotate(dcount=Count('report_type')), key=lambda k: k['dcount'], reverse=True)
    reports_by_report_type_last_month = sorted(CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month).values('report_type').annotate(dcount=Count('report_type')), key=lambda k: k['dcount'], reverse=True)

    reports_by_report_type = []
    for report_data in reports_by_report_type_this_month:
        if report_data['report_type'] is not None:
            reports_by_report_type.append((
                report_data['report_type'],
                [i[1] for i in CSSCall.REPORT_TYPE_CHOICES if report_data['report_type'] == i[0]][0],
                report_data['dcount'],
                [i['dcount'] for i in reports_by_report_type_last_month if i['report_type'] == report_data['report_type']] and [i['dcount'] for i in reports_by_report_type_last_month if i['report_type'] == report_data['report_type']] or 0
            ))

    for report_data in reports_by_report_type_last_month:
        if report_data['report_type'] is not None:
            if report_data['report_type'] not in [i[0] for i in reports_by_report_type]:
                reports_by_report_type.append((
                    report_data['report_type'],
                    [i[1] for i in CSSCall.REPORT_TYPE_CHOICES if report_data['report_type'] == i[0]][0],
                    0,
                    report_data['dcount']
                ))

    reports_by_report_type.append((
        -1,
        'Unknown',
        CSSCall.objects.filter(reported_datetime__gte=start_of_month, report_type__isnull=True).count(),
        CSSCall.objects.filter(reported_datetime__gte=start_of_last_month, reported_datetime__lt=start_of_month, report_type__isnull=True).count()
    ))

    return render(
        request,
        'workflow/landing.html',
        {
            'current_month_new_reports': current_month_new_reports,
            'last_month_new_reports': last_month_new_reports,
            'current_month_new_cases': current_month_new_cases,
            'last_month_new_cases': last_month_new_cases,
            'resolved_cases_this_month': resolved_cases_this_month,
            'resolved_cases_last_month': resolved_cases_last_month,
            'report_ids': json.dumps(list(CSSCall.objects.filter(reported_datetime__gte=two_weeks_ago).order_by('-reported_datetime').values_list('id', flat=True))),
            'reports_by_source': reports_by_source,
            'reports_by_report_type': reports_by_report_type,
            'case_actions': case_actions,
            'recent_reports': recent_reports,
            'verifications_in_progress_this_month': verifications_in_progress_this_month,
            'verifications_in_progress_last_month': verifications_in_progress_last_month
        }
    )


@login_required(login_url='/login/')
def get_notifications(request):
    formatted_notifications = []

    for notification in StaffReportNotification.objects.filter(to_user=request.user, sent_at__isnull=True):
        formatted_notifications.append({
            'report_id': notification.report.id,
            'message': "{} forwarded you a report{} (click to view)".format(
                notification.from_user.get_full_name(),
                notification.report.get_address() and ' involving ' + notification.report.get_address() or ''
            )
        })

    return JsonResponse({'notifications': formatted_notifications})


@login_required(login_url='/login/')
def mark_notifications_seen(request):
    now = pytz.timezone('America/Los_Angeles').localize(datetime.now())
    StaffReportNotification.objects.filter(to_user=request.user, sent_at__isnull=True).update(sent_at=now)

    return JsonResponse({'status': 'OK'})


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
                return HttpResponseRedirect('/workflow')
            else:
                messages.add_message(request, messages.WARNING, "This user account is disabled.")
        else:
            messages.add_message(request, messages.WARNING, "The user nane or password is incorrect.")
    else:
        users = User.objects.filter(id=request.user.id)
        user = users and users[0]
        if user and user.is_authenticated:
            return HttpResponseRedirect('/workflow')

    return render(request, 'workflow/login.html', {'exclude_navbar': True})
