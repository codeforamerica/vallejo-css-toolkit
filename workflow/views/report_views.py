import logging
import traceback

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse

from common.datatables import get_datatables_data

from intake.models import CallAuditItem, PublicUploadedAsset

from workflow.forms.report_forms import ReportForm
from workflow.models import CSSCall, CSSCase, Verification
from workflow.sql import CALLS_DATA_SQL, CALLS_IDX_COLUMN_MAP
from workflow.utils import get_location_history, get_reports

log = logging.getLogger('consolelogger')

LOG_AUDIT_HISTORY = False


@login_required(login_url='/admin/login/')
def add_report(request):
    form = ReportForm(request.POST or None)

    if form.errors:
        messages.add_message(request, messages.ERROR, form.errors)

    if form.is_valid():
        report = form.save()
        messages.add_message(request, messages.SUCCESS, 'Report successfully Added. You can access it <a href=/workflow/report/{}>here</a>'.format(report.id), extra_tags='safe')
        if request.POST.get('next-action') == "Another report":
            return HttpResponseRedirect('/workflow/add_report')

        else:
            return HttpResponseRedirect('/workflow/reports')

    return render(request, 'workflow/add_report.html', {'form': form})


@login_required(login_url='/admin/login/')
def report(request, report_id):
    instance = get_object_or_404(CSSCall, id=report_id)
    form = ReportForm(request.POST or None, instance=instance)

    if form.errors:
        messages.add_message(request, messages.ERROR, form.errors)

    if form.is_valid():
        call = form.save()
        messages.add_message(request, messages.SUCCESS, 'Report successfully updated. You can access it <a href=/workflow/report/{}>here</a>'.format(call.id), extra_tags='safe')

        if LOG_AUDIT_HISTORY:
            # TODO: refactor and enable this

            user = get_object_or_404(User, id=request.user.id)
            for field, new_value in form.cleaned_data.iteritems():
                old_value = form.initial.get(field)

                if (old_value or new_value) and old_value != new_value:
                    CallAuditItem.objects.create(user=user, call=call, changed_field=field, old_value=old_value, new_value=new_value)

        if request.POST.get('next-action') == 'Move to Verification':
            if not Verification.objects.filter(report=call):
                verification = Verification.objects.create(report=call)
            else:
                verification = Verification.objects.filter(report=call)[0]
                # add message warning that it exists

            return HttpResponseRedirect('/workflow/verification/{}'.format(verification.id))

        # TODO: handle other conditions
        else:
            return HttpResponseRedirect('/workflow/reports')

    # either the form was not valid, or we're just loading the page
    location_history = get_location_history(instance.address_number, instance.street_name)

    # TODO: refactor since we're not using typeform anymore
    external_assets = PublicUploadedAsset.objects.filter(css_report=instance.id).order_by('-id')
    external_assets_count = len(external_assets)

    verification_id = None
    case_id = None

    verifications = Verification.objects.filter(report=instance)
    if verifications:
        verification = verifications[0]
        verification_id = verification.id
        cases = CSSCase.objects.filter(verification=verification)
        if cases:
            case_id = cases[0].id

    return render(
        request,
        'workflow/report.html',
        {
            'id': instance.id,
            'form': form,
            'location_history': location_history,
            'external_assets': external_assets,
            'external_assets_count': external_assets_count,
            'verification_id': verification_id,
            'case_id': case_id
        }
    )


@login_required(login_url='/admin/login/')
def reports_data(request):
    request_dict = dict(request.GET.items())

    try:
        results = get_datatables_data(request_dict, CALLS_DATA_SQL, CALLS_IDX_COLUMN_MAP)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)


@login_required(login_url='/admin/login/')
def reports(request):
    if request.method == "GET":
        reports_data, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset = get_reports(request.GET)

        return render(
            request,
            'workflow/reports.html',
            {
                'reports_data': reports_data,
                'pagination_keys': pagination_keys,
                'active_page_number': page_idx + 1,
                'sort_order': sort_order,
                'sort_key': sort_key,
                'limit': limit,
                'offset': offset,
                'search_get_param': search_get_param
            }
        )

    elif request.method == "POST":
        to_delete_ids = request.POST.getlist('to_delete')
        if to_delete_ids:
            for id_string in to_delete_ids:
                report = CSSCall.objects.get(id=int(id_string))
                report.active = False
                report.save()
        messages.add_message(request, messages.INFO, 'Successfully deleted {} report{}.'.format(len(to_delete_ids), len(to_delete_ids) > 1 and "s" or ""))
        # TODO: catch exceptions and message error

        previous_url_params = {
            'sort_key': request.POST.get('sort_key'),
            'sort_order': request.POST.get('sort_order'),
            'offset': request.POST.get('offset'),
            'limit': request.POST.get('limit'),
            'search': request.POST.get('search_get_param'),
        }

        url_params = "?" + "&".join(["{}={}".format(k, v) for k, v in previous_url_params.iteritems() if v not in ('None', '', None)])

        return HttpResponseRedirect('/workflow/reports/{}'.format(url_params))
