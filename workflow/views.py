from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from workflow.models import PDCase, CSSCase
from geo.utils.normalize_address import normalize_address_string
from geo.utils.geocode import geocode

import logging

logger = logging.getLogger('consolelogger')

def process_case_data(cases):
    results = []
    for case in cases:
        normalized = normalize_address_string(case.raw_address)
        if not normalized:
            logger.info('NORMALIZER_MISS: {}'.format(case.raw_address))
            continue

        street_number, street_name, street_descriptor = normalized
        coords = geocode(street_number, street_name, street_descriptor)
        if coords:
            results.append({'lat': coords['lat'], 'lng': coords['lng']})
        else:
            logger.info('GEOCODE_MISS - {}|{}|{}'.format(street_number, street_name, street_descriptor))

    return JsonResponse({'results': results})

# @login_required
def css_data(request):
    cases = CSSCase.objects.filter()
    return process_case_data(cases)

# @login_required
def rms_data(request):
    cases = PDCase.objects.filter()
    return process_case_data(cases)

# @login_required
def map_view(request):

    return render(request, 'workflow/map.html')

@login_required
def location_view(request, location_id):
    instance = get_object_or_404(Location, id=location_id)

    return render(request, 'workflow/location.html', {'location': instance})
