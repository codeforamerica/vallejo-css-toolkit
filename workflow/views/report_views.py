import logging
# import traceback

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from intake.models import CallAuditItem, PublicUploadedAsset

from workflow.forms.report_forms import ReportForm
from workflow.models import CSSCall, CSSCase, Verification, CSSReportView, ReportNotification, Recording, StaffReportNotification
from workflow.utils import get_location_history, get_reports

log = logging.getLogger('consolelogger')

LOG_AUDIT_HISTORY = False


@login_required(login_url='/login/')
def add_report(request):
    readonly = not (request.user.is_staff or request.user.is_superuser)
    form = ReportForm(request.POST or None, readonly=readonly)
    log.info(request.POST)

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


@login_required(login_url='/login/')
def report(request, report_id):
    instance = get_object_or_404(CSSCall, id=report_id)
    CSSReportView.objects.create(css_report=instance, user=request.user)

    readonly = not (request.user.is_staff or request.user.is_superuser)
    form = ReportForm(request.POST or None, readonly=readonly, instance=instance)

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

            return HttpResponseRedirect('/workflow/verify_report/{}'.format(verification.id))

        elif request.POST.get('next-action') == 'Forward':
            return HttpResponseRedirect('/workflow/forward_report/{}'.format(call.id))

        elif request.POST.get('next-action') == 'Resolve':
            return HttpResponseRedirect('/workflow/resolve_report/{}'.format(call.id))

        else:  # we're just saving the report
            return HttpResponseRedirect('/workflow/reports')

    # either the form was not valid, or we're just loading the page
    location_history = get_location_history(instance.address_number, instance.street_name, instance.id)
    external_assets = PublicUploadedAsset.objects.filter(css_report=instance.id).order_by('-id')
    external_assets_count = len(external_assets)

    name_recording = Recording.objects.filter(call=instance, type=Recording.NAME)
    location_recording = Recording.objects.filter(call=instance, type=Recording.LOCATION)
    description_recording = Recording.objects.filter(call=instance, type=Recording.DESCRIPTION)
    email_recording = Recording.objects.filter(call=instance, type=Recording.EMAIL)
    duration_recording = Recording.objects.filter(call=instance, type=Recording.DURATION)
    address_recording = Recording.objects.filter(call=instance, type=Recording.ADDRESS)
    time_of_day_recording = Recording.objects.filter(call=instance, type=Recording.TIME_OF_DAY)

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
            'case_id': case_id,
            'name_recording': name_recording,
            'location_recording': location_recording,
            'description_recording': description_recording,
            'email_recording': email_recording,
            'duration_recording': duration_recording,
            'address_recording': address_recording,
            'time_of_day_recording': time_of_day_recording
        }
    )


@login_required(login_url='/login/')
def verify_report(request, verification_id):
    if request.method == 'POST':
        verification = get_object_or_404(Verification, id=verification_id)
        message = request.POST.get('message')
        if message:
            ReportNotification.objects.create(report=verification.report, message=message)
            messages.add_message(request, messages.SUCCESS, "Successfully scheduled outgoing message to reporter.")

        return HttpResponseRedirect('/workflow/verification/{}'.format(verification.id))

    else:
        return render(
            request,
            'workflow/message_reporter.html',
            {
                'default_message': 'The issue you reported has been moved to the next step in the investigation.',
                'title': "Verify Report",
                'cancel_url': '/workflow/verification/{}'.format(verification_id)
            }
        )


@login_required(login_url='/login/')
def resolve_report(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(CSSCall, id=report_id)
        message = request.POST.get('message')
        if message:
            ReportNotification.objects.create(report=report, message=message)
            messages.add_message(request, messages.SUCCESS, "Successfully scheduled outgoing message to reporter.")

        return HttpResponseRedirect('/workflow/reports/')

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
def forward_report(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(CSSCall, id=report_id)
        message = request.POST.get('message')
        to_user_id = request.POST.get('to_user_id')
        if message:
            StaffReportNotification.objects.create(report=report, message=message, from_user=request.user, to_user=User.objects.get(id=to_user_id))
            messages.add_message(request, messages.SUCCESS, "Successfully forwarded report to recipient.")

        return HttpResponseRedirect('/workflow/reports/')

    else:
        return render(
            request,
            'workflow/message_reporter.html',
            {
                'users': User.objects.filter(is_active=True).exclude(id=request.user.id),
                'forward': True,
                'default_message': 'Please take a look at this report. Thank you.',
                'title': "Resolve Report",
                'cancel_url': '/workflow/reports/'
            }
        )


@login_required(login_url='/login/')
def reports(request):
    if request.method == "GET":
        reports_data, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset = get_reports(request.GET)

        # reports_data = []
        return render(
            request,
            'workflow/reports.html',
            {
                'reports_data': reports_data,
                'pagination_keys': pagination_keys,
                'active_page_number': page_idx and page_idx + 1 or 1,
                'sort_order': sort_order,
                'sort_key': sort_key,
                'limit': limit,
                'offset': offset,
                'page_start': offset + 1,
                'page_end': min(limit + offset, reports_data and reports_data[0][7] or limit + offset),
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
