import os
import requests
import urllib
import logging
import tempfile
import traceback

import boto
from boto.s3.key import Key

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from workflow.models import Verification, CSSCase, VerificationContactAction, UploadedAsset, CSSCall, VerificationView, ReportNotification, StaffReportNotification
from workflow.forms.verification_forms import PropertyDetailsForm, UploadAssetForm

log = logging.getLogger('consolelogger')


@login_required(login_url='/login/')
def verification(request, verification_id):
    instance = get_object_or_404(Verification, id=verification_id)
    VerificationView.objects.create(verification=instance, user=request.user)

    readonly = not (request.user.is_staff or request.user.is_superuser)
    property_details_form = PropertyDetailsForm(request.POST or None, request.FILES or None, readonly=readonly, instance=instance)
    uploaded_asset_form = UploadAssetForm(request.POST, request.FILES)

    if property_details_form.errors:
        messages.add_message(request, messages.ERROR, property_details_form.errors)

    if property_details_form.is_valid():
        verification = property_details_form.save()
        try:
            conn = boto.connect_s3()
            b = conn.get_bucket('vallejo-css-toolkit')

            if property_details_form.files.get('uploaded_asset'):
                fname = property_details_form.files.get('uploaded_asset').name
                tmpfile = tempfile.NamedTemporaryFile(delete=False)
                for chunk in property_details_form.files['uploaded_asset'].chunks():
                    tmpfile.write(chunk)
                tmpfile.close()

                env = os.environ.get('DJANGO_SETTINGS_MODULE', 'not_set')

                k = Key(b)
                k.key = 'uploaded-assets/{}/{}/{}'.format(
                    env.split('.')[-1],
                    verification.id,
                    tmpfile.name.split('/')[-1]
                )
                k.set_contents_from_filename(tmpfile.name)
                UploadedAsset.objects.create(verification=verification, fname=fname, fpath=k.key)

        except:
            log.error("Encountered exception attempting to upload submitted file: {}".format(traceback.format_exc()))

        if request.POST.get('next-action') == 'Move to Case':
            if not CSSCase.objects.filter(verification=verification):
                case = CSSCase.objects.create(verification=verification)
            else:
                case = CSSCase.objects.create(verification=verification)[0]
            return HttpResponseRedirect('/workflow/case/{}'.format(case.id))

        elif request.POST.get('next-action') == 'Forward':
            return HttpResponseRedirect('/workflow/forward_verification/{}'.format(verification.id))

        elif request.POST.get('next-action') == 'Resolve':
            return HttpResponseRedirect('/workflow/resolve_verification/{}'.format(verification.id))

        elif request.POST.get('next-action') == 'Revert to Report':
            return HttpResponseRedirect('/workflow/revert_verification/{}'.format(verification.id))

        else:  # we're just saving the verification
            messages.add_message(request, messages.SUCCESS, 'Verification successfully updated.')
            return HttpResponseRedirect('/workflow/verification/{}'.format(verification.id))

    # either the form was invalid or we're just loading the page
    case_id = None
    cases = CSSCase.objects.filter(verification=instance)
    if cases:
        case_id = cases[0].id

    uploaded_docs = UploadedAsset.objects.filter(verification=instance).order_by('timestamp')
    contact_log = VerificationContactAction.objects.filter(verification=instance).order_by('timestamp').values_list('timestamp', 'contacter_name', 'contact_type', 'contact_description')
    contact_log = [[i[0].strftime('%m/%d/%y')] + list(i[1:]) for i in contact_log]

    return render(
        request,
        'workflow/verification.html',
        {
            'property_details_form': property_details_form,
            'uploaded_docs': uploaded_docs,
            'property_address': instance.report.get_address(),
            'verification_id': instance.pk,
            'report_id': instance.report.id,
            'case_id': case_id,
            'contact_log': contact_log,
            'uploaded_asset_form': uploaded_asset_form,
            'report': instance.report
        }
    )


@login_required(login_url='/login/')
def revert_verification(request, verification_id):
    verification = get_object_or_404(Verification, id=verification_id)
    report = verification.report

    for case in CSSCase.objects.filter(verification=verification):
        case.delete()

    verification.delete()
    messages.add_message(request, messages.SUCCESS, "Successfully reverted verification to report stage.")
    return HttpResponseRedirect('/workflow/report/{}'.format(report.id))


@login_required(login_url='/login/')
def resolve_verification(request, verification_id):
    if request.method == 'POST':
        verification = get_object_or_404(Verification, id=verification_id)
        message = request.POST.get('message')
        if message:
            ReportNotification.objects.create(report=verification.report, message=message)
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
def forward_verification(request, verification_id):
    if request.method == 'POST':
        verification = get_object_or_404(Verification, id=verification_id)
        message = request.POST.get('message')
        to_user_id = request.POST.get('to_user_id')
        if message:
            StaffReportNotification.objects.create(report=verification.report, message=message, from_user=request.user, to_user=User.objects.get(id=to_user_id))
            messages.add_message(request, messages.SUCCESS, "Successfully forwarded report to recipient.")

        return HttpResponseRedirect('/workflow/reports/')

    else:
        return render(
            request,
            'workflow/message_reporter.html',
            {
                'users': User.objects.filter(is_active=True).exclude(id=request.user.id),
                'forward': True,
                'default_message': 'Please take a look at this verification. Thank you.',
                'title': "Resolve Report",
                'cancel_url': '/workflow/reports/'
            }
        )


@login_required(login_url='/login/')
def add_contact_action(request):
    verification_id = request.POST.get('verification_id')
    contacter_name = request.POST.get('contacter_name')
    contact_type = request.POST.get('contact_type')
    contact_description = request.POST.get('contact_description')

    verification = Verification.objects.get(id=verification_id)

    vca = VerificationContactAction.objects.create(
        verification=verification,
        contacter_name=contacter_name,
        contact_type=contact_type,
        contact_description=contact_description
    )

    return JsonResponse({
        'timestamp': vca.timestamp.strftime('%m/%d/%Y'),
        'contacter_name': vca.contacter_name,
        'contact_type': vca.contact_type,
        'contact_description': vca.contact_description,
    })


@login_required(login_url='/login/')
def geocode_address(request):
    report_id = request.GET.get('report_id')
    lat, lon = None, None

    if report_id:
        report = get_object_or_404(CSSCall, id=report_id)

        params = urllib.urlencode({
            'street': report.get_address(),
            'city': 'Vallejo',
            'state': 'CA',
            'benchmark': '4',
            'format': 'json'
        })
        url = "http://geocoding.geo.census.gov/geocoder/locations/address?{}".format(params)

        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                results = r.json()
                status = 'unable to geocode address'
                if "result" in results:
                    if "addressMatches" in results["result"] and len(results["result"]["addressMatches"]) > 0:
                        if "coordinates" in results["result"]["addressMatches"][0]:
                            lat = results["result"]["addressMatches"][0]["coordinates"].get("y")
                            lon = results["result"]["addressMatches"][0]["coordinates"].get("x")
                            status = 'successful census geocode lookup'

            else:
                status = 'Unsuccessful census geocode lookup'

        except requests.exceptions.Timeout:
            log.warning("Geocode timeout")
            status = 'geocode timeout'

    else:
        status = 'No report id provided in request'

    return JsonResponse({'status': status, 'lat': lat, 'lon': lon})
