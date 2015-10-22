import traceback
import logging
from django.contrib import messages

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from common.datatables import get_datatables_data
from workflow.models import CSSCase, CSSCaseAssignee

from workflow.forms.case_forms import CSSCaseDetailsForm, CSSCaseOwnerForm
from workflow.sql import CSS_CASES_DATA_SQL, CSS_CASES_IDX_COLUMN_MAP

log = logging.getLogger('consolelogger')


@login_required(login_url='/admin/login/')
def cases_data(request):
    request_dict = dict(request.GET.items())

    try:
        results = get_datatables_data(request_dict, CSS_CASES_DATA_SQL, CSS_CASES_IDX_COLUMN_MAP)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)


@login_required(login_url='/admin/login/')
def cases(request):
    return render(request, 'workflow/cases.html')


@login_required(login_url='/admin/login/')
def visit_queue_data(request):
    results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}
    return JsonResponse(results)


@login_required(login_url='/admin/login/')
def visit_queue(request):
    return render(request, 'workflow/visit_queue.html')


@login_required(login_url='/admin/login/')
def case(request, case_id):
    instance = get_object_or_404(CSSCase, id=case_id)
    case_details_form = CSSCaseDetailsForm(request.POST or None, instance=instance)

    contact_owner_form = CSSCaseOwnerForm(request.POST or None, instance=instance)

    uploaded_docs = [
        {"name": 'Lease Agreement 2015', "filename": 'lease2015.pdf', "added": "Jan. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Deed with signature', "filename": 'deed_updated.pdf', "added": "Sep, 16, 2015", "thumbnail_url": "http://placehold.it/120x120"},
        {"name": 'Notice to evict - copy', "filename": 'eviction_notice_9_1_15.pdf', "added": "Sep. 1, 2015", "thumbnail_url": "http://placehold.it/120x120"}
    ]

    if case_details_form.is_valid():
        case = case_details_form.save()
        messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')

        return HttpResponseRedirect('/workflow/case/%d' % case.id)

    if contact_owner_form.is_valid():
        case = contact_owner_form.save()
        messages.add_message(request, messages.SUCCESS, 'Case successfully updated.')

        return HttpResponseRedirect('/workflow/case/%d' % case.id)

    return render(
        request,
        'workflow/case.html',
        {
            'case_assignees': CSSCaseAssignee.objects.filter(case=instance).values_list('assignee_name', flat=True),
            'case_details_form': case_details_form,
            'contact_owner_form': contact_owner_form,
            'uploaded_docs': uploaded_docs,
            'property_address': "{} {}".format(instance.address_number, instance.street_name.capitalize()),
            'case_id': instance.pk
        }
    )


@login_required(login_url='/admin/login/')
def add_case_assignee(request):
    case_id = request.POST.get('case_id')
    assignee = request.POST.get('assignee')

   # add to the database
    CSSCaseAssignee.objects.get_or_create(assignee_name=assignee, case=get_object_or_404(CSSCase, id=case_id))

    return JsonResponse({'status': 'OK'})


@login_required(login_url='/admin/login/')
def remove_case_assignee(request):
    case_id = request.POST.get('case_id')
    assignee = request.POST.get('assignee')

   # remove from the database
    CSSCaseAssignee.objects.filter(
        assignee_name=assignee,
        case=get_object_or_404(
            CSSCase,
            id=case_id
        )
    ).delete()

    return JsonResponse({'status': 'OK'})
