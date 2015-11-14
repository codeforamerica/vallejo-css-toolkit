import requests
import urllib
import logging
from django.contrib import messages

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from workflow.models import Verification, CSSCase, VerificationContactAction, UploadedAsset
from workflow.forms.verification_forms import PropertyDetailsForm, UploadAssetForm

log = logging.getLogger('consolelogger')


@login_required(login_url='/login/')
def verification(request, verification_id):
    instance = get_object_or_404(Verification, id=verification_id)

    property_details_form = PropertyDetailsForm(request.POST or None, instance=instance)
    uploaded_asset_form = UploadAssetForm(request.POST, request.FILES)

    if property_details_form.errors:
        messages.add_message(request, messages.ERROR, property_details_form.errors)

    if property_details_form.is_valid():
        verification = property_details_form.save()
        messages.add_message(request, messages.SUCCESS, 'Verification successfully updated.')

        if request.POST.get('next-action') == 'Move to Case':
            if not CSSCase.objects.filter(verification=verification):
                case = CSSCase.objects.create(verification=verification)
            else:
                case = CSSCase.objects.create(verification=verification)[0]
                # add message warning that it exists
            return HttpResponseRedirect('/workflow/case/{}'.format(case.id))

        # TODO: handle other conditions
        else:
            return HttpResponseRedirect('/workflow/verification/{}'.format(verification.id))

    # either the form was invalid or we're just loading the page
    case_id = None
    cases = CSSCase.objects.filter(verification=instance)
    if cases:
        case_id = cases[0].id

    uploaded_docs = UploadedAsset.objects.filter(verification=instance).order_by('timestamp').values_list('timestamp', 'fname', 'fpath')
    uploaded_docs = [[i[0].strftime('%m/%d/%y')] + list(i[1:]) for i in uploaded_docs]

    contact_log = VerificationContactAction.objects.filter(verification=instance).order_by('timestamp').values_list('timestamp', 'contacter_name', 'contact_type', 'contact_description')
    contact_log = [[i[0].strftime('%m/%d/%y')] + list(i[1:]) for i in contact_log]

    params = urllib.urlencode({
        'street': instance.report.get_address(),
        'city': 'Vallejo',
        'state': 'CA',
        'benchmark': '4',
        'format': 'json'
    })
    url = "http://geocoding.geo.census.gov/geocoder/locations/address?{}".format(params)
    lat, lon = None, None

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            results = r.json()
            if "result" in results:
                if "addressMatches" in results["result"]:
                    if "coordinates" in results["result"]["addressMatches"][0]:
                        lat = results["result"]["addressMatches"][0]["coordinates"].get("y")
                        lon = results["result"]["addressMatches"][0]["coordinates"].get("x")

    except requests.exceptions.Timeout:
        log.warning("Geocode timeout")

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
            'lat': lat,
            'lon': lon
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
