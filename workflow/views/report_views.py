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
from intake.models import CallAuditItem, TypeformAsset

from workflow.forms.report_forms import ReportForm
from workflow.models import CSSCall, PDCase, CRWCase, CSSCase, Verification
from workflow.sql import CALLS_DATA_SQL, AUDIT_LOG_DATA_SQL, CALLS_IDX_COLUMN_MAP, AUDIT_LOG_IDX_COLUMN_MAP

log = logging.getLogger('consolelogger')

LOG_AUDIT_HISTORY = False


@login_required(login_url='/admin/login/')
def add_report(request):
    form = ReportForm(request.POST or None, initial={'reported_datetime': datetime.now()})
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Report successfully added.')

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
        messages.add_message(request, messages.SUCCESS, 'Report successfully updated.')

        if LOG_AUDIT_HISTORY:

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
        reports = CSSCall.objects.filter(address=instance.address).values_list('id', 'reported_datetime')
    else:
        reports = [(instance.id, instance.reported_datetime)]

    external_assets = TypeformAsset.objects.filter(css_report=instance.id).order_by('-id')
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

    # TODO: fix the history section at db and view level
    return render(
        request,
        'workflow/report.html',
        {
            'id': instance.id,
            'form': form,
            'css_cases': css_cases,
            'external_cases': list(chain(pd_cases, crw_cases)),
            'reports': reports,
            'external_assets': external_assets,
            'external_assets_count': external_assets_count,
            'verification_id': verification_id,
            'case_id': case_id
        }
    )


@login_required(login_url='/admin/login/')
def call_audit_log_data(request):
    request_dict = dict(request.GET.items())

    try:
        results = get_datatables_data(request_dict, AUDIT_LOG_DATA_SQL, AUDIT_LOG_IDX_COLUMN_MAP)
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc().replace('\n', '\t')))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)


@login_required(login_url='/admin/login/')
def call_audit_log(request):
    return render(request, 'workflow/call_audit_log.html')


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
    return render(request, 'workflow/reports.html')
