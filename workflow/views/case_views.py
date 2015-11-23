import traceback
import logging
from django.contrib import messages

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from common.datatables import get_datatables_data
from workflow.models import CSSCase, CSSCaseAssignee

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

    readonly = not (request.user.is_staff or request.user.is_superuser)
    case_details_form = CSSCaseDetailsForm(request.POST or None, readonly=readonly, instance=instance)

    if case_details_form.errors:
        messages.add_message(request, messages.ERROR, case_details_form.errors)

    if case_details_form.is_valid():
        case = case_details_form.save()
        messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')

        return HttpResponseRedirect('/workflow/case/%d' % case.id)

    return render(
        request,
        'workflow/case.html',
        {
            'case_assignees': CSSCaseAssignee.objects.filter(case=instance).values_list('assignee_name', flat=True),
            'case_details_form': case_details_form,
            'property_address': instance.verification.report.get_address(),
            'case_id': instance.pk,
            'verification_id': instance.verification.id,
            'report_id': instance.verification.report.id,
            'report': instance.verification.report
        }
    )


@login_required(login_url='/login/')
def add_case_assignee(request):
    case_id = request.POST.get('case_id')
    assignee = request.POST.get('assignee')
    CSSCaseAssignee.objects.get_or_create(assignee_name=assignee, case=get_object_or_404(CSSCase, id=case_id))

    return JsonResponse({'status': 'OK'})


@login_required(login_url='/login/')
def remove_case_assignee(request):
    print request.POST

    case_id = request.POST.get('case_id')
    assignee = request.POST.get('assignee')

    CSSCaseAssignee.objects.filter(
        assignee_name=assignee,
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
        if user.first_name and user.last_name:
            users.append('{} {}'.format(user.first_name, user.last_name))
        elif user.first_name:
            users.append('{}'.format(user.first_name))
        elif user.last_name:
            users.append('{}'.format(user.last_name))

    return JsonResponse({'users': users})
