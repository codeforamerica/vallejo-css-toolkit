import traceback
import logging
from datetime import datetime

import pytz

from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from common.datatables import get_datatables_data
from workflow.models import CSSCase, CSSCaseAssignee, ReportNotification, StaffReportNotification, CaseView

from workflow.forms.case_forms import CSSCaseDetailsForm  # , CSSCaseOwnerForm
from workflow.sql import CSS_CASES_DATA_SQL, CSS_CASES_IDX_COLUMN_MAP
from workflow.utils import get_cases

log = logging.getLogger('consolelogger')


# TODO: deprecate
@login_required(login_url='/login/')
def cases_data(request):
    request_dict = dict(request.GET.items())

    try:
        results = get_datatables_data(request_dict, CSS_CASES_DATA_SQL, CSS_CASES_IDX_COLUMN_MAP)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)


@login_required(login_url='/login/')
def cases(request):
    if request.method == "GET":
        cases_data, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset = get_cases(request.GET)

        # cases_data = []
        return render(
            request,
            'workflow/cases.html',
            {
                'cases_data': cases_data,
                'pagination_keys': pagination_keys,
                'active_page_number': page_idx and page_idx + 1 or 1,
                'sort_order': sort_order,
                'sort_key': sort_key,
                'limit': limit,
                'offset': offset,
                'page_start': offset + 1,
                'page_end': min(limit + offset, cases_data and cases_data[0][8] or limit + offset),
                'search_get_param': search_get_param
            }
        )

    elif request.method == "POST":
        to_delete_ids = request.POST.getlist('to_delete')
        if to_delete_ids:
            for id_string in to_delete_ids:
                report = CSSCase.objects.get(id=int(id_string))
                report.active = False
                report.save()
        messages.add_message(request, messages.INFO, 'Successfully deleted {} case{}.'.format(len(to_delete_ids), len(to_delete_ids) > 1 and "s" or ""))
        # TODO: catch exceptions and message error

        previous_url_params = {
            'sort_key': request.POST.get('sort_key'),
            'sort_order': request.POST.get('sort_order'),
            'offset': request.POST.get('offset'),
            'limit': request.POST.get('limit'),
            'search': request.POST.get('search_get_param'),
        }

        url_params = "?" + "&".join(["{}={}".format(k, v) for k, v in previous_url_params.iteritems() if v not in ('None', '', None)])

        return HttpResponseRedirect('/workflow/cases/{}'.format(url_params))


@login_required(login_url='/login/')
def case(request, case_id):
    instance = get_object_or_404(CSSCase, id=case_id)
    CaseView.objects.create(case=instance, user=request.user)

    readonly = not (request.user.is_staff or request.user.is_superuser)
    case_details_form = CSSCaseDetailsForm(request.POST or None, readonly=readonly, instance=instance)

    if case_details_form.errors:
        messages.add_message(request, messages.ERROR, case_details_form.errors)

    if case_details_form.is_valid():
        case = case_details_form.save()

        if request.POST.get('next-action') == 'Forward':
            return HttpResponseRedirect('/workflow/forward_verification/{}'.format(case.id))

        elif request.POST.get('next-action') == 'Resolve':
            return HttpResponseRedirect('/workflow/resolve_case/{}'.format(case.id))

        elif request.POST.get('next-action') == 'Revert to Verification':
            return HttpResponseRedirect('/workflow/revert_case/{}'.format(case.id))

        else:  # we're just saving the case
            messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')
            return HttpResponseRedirect('/workflow/case/{}'.format(case.id))

    return render(
        request,
        'workflow/case.html',
        {
            'case_assignees': [ca.assignee_user.get_full_name() for ca in instance.csscaseassignee_set.all()],
            'case_details_form': case_details_form,
            'property_address': instance.verification.report.get_address(),
            'case_id': instance.pk,
            'verification_id': instance.verification.id,
            'report_id': instance.verification.report.id,
            'report': instance.verification.report
        }
    )


@login_required(login_url='/login/')
def revert_case(request, case_id):
    case = get_object_or_404(CSSCase, id=case_id)
    verification = case.verification
    case.delete()
    messages.add_message(request, messages.SUCCESS, "Successfully reverted case to verification stage.")
    return HttpResponseRedirect('/workflow/verification/{}'.format(verification.id))


@login_required(login_url='/login/')
def resolve_case(request, case_id):
    if request.method == 'POST':
        case = get_object_or_404(CSSCase, id=case_id)
        message = request.POST.get('message')
        now = pytz.timezone('America/Los_Angeles').localize(datetime.now())
        case.resolved_at = now
        case.save()

        if message:
            ReportNotification.objects.create(report=case.verification.report, message=message)
            messages.add_message(request, messages.SUCCESS, "Successfully scheduled outgoing message to reporter.")

        return HttpResponseRedirect('/workflow/cases/')

    else:
        return render(
            request,
            'workflow/message_reporter.html',
            {
                'default_message': 'The issue you reported was resolved. Thank you!',
                'title': "Resolve Report",
                'cancel_url': '/workflow/reports/'
            }
        )


@login_required(login_url='/login/')
def forward_case(request, case_id):
    if request.method == 'POST':
        case = get_object_or_404(CSSCase, id=case_id)
        message = request.POST.get('message')
        to_user_id = request.POST.get('to_user_id')
        if message:
            StaffReportNotification.objects.create(report=case.verification.report, message=message, from_user=request.user, to_user=User.objects.get(id=to_user_id))
            messages.add_message(request, messages.SUCCESS, "Successfully forwarded report to recipient.")

        return HttpResponseRedirect('/workflow/cases/')

    else:
        return render(
            request,
            'workflow/message_reporter.html',
            {
                'users': User.objects.filter(is_active=True).exclude(id=request.user.id),
                'forward': True,
                'default_message': 'Please take a look at this case. Thank you.',
                'title': "Resolve Report",
                'cancel_url': '/workflow/reports/'
            }
        )


@login_required(login_url='/login/')
def add_case_assignee(request):
    case_id = request.POST.get('case_id')
    assignee_name = request.POST.get('assignee')
    assignee_users = [u for u in User.objects.filter(is_active=True) if u.get_full_name() == assignee_name]
    for assignee_user in assignee_users:
        CSSCaseAssignee.objects.get_or_create(assignee_user=assignee_user, case=get_object_or_404(CSSCase, id=case_id))

    return JsonResponse({'status': 'OK'})


@login_required(login_url='/login/')
def remove_case_assignee(request):

    case_id = request.POST.get('case_id')
    assignee_name = request.POST.get('assignee')
    assignee_users = [u for u in User.objects.filter(is_active=True) if u.get_full_name() == assignee_name]
    for assignee_user in assignee_users:

        CSSCaseAssignee.objects.filter(
            assignee_user=assignee_user,
            case=get_object_or_404(
                CSSCase,
                id=case_id
            )
        ).delete()

    return JsonResponse({'status': 'OK'})


@login_required(login_url='/login/')
def get_case_assignees(request):
    users = []
    for user in User.objects.filter(is_active=True):
        users.append('{}'.format(user.get_full_name()))

    return JsonResponse({'users': users})
