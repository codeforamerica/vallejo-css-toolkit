import string
import operator
from itertools import chain

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from geo.utils.geocode import geocode
from workflow.models import PDCase, CSSCase
from geo.utils.normalize_address import normalize_address_string, combine_address_parts

import logging

log = logging.getLogger('consolelogger')


def process_case_data(cases):
    results = []
    for case in cases:
        normalized = normalize_address_string(case.raw_address)
        if not normalized:
            log.info('NORMALIZER_MISS: {}'.format(case.raw_address))
            continue

        street_number, street_name, street_descriptor = normalized
        coords = geocode(street_number, street_name, street_descriptor)
        if coords:
            results.append({'lat': coords['lat'], 'lng': coords['lng']})
        else:
            log.info('GEOCODE_MISS - {}|{}|{}'.format(street_number, street_name, street_descriptor))

    return JsonResponse({'results': results})

@login_required
def css_data(request):
    cases = CSSCase.objects.filter()
    return process_case_data(cases)

@login_required
def rms_data(request):
    cases = PDCase.objects.filter()
    return process_case_data(cases)

@login_required
def map_view(request):

    return render(request, 'workflow/map.html')

def filter_location_data(case, street_number, street_name, street_descriptor):
    normalized = normalize_address_string(case.raw_address)
    if normalized and normalized[0] == street_number and normalized[1] == street_name:
        return [case.id]
    return []

@login_required
def location_data(request):
    results = []

    street_number = request.GET.get('street_number')
    street_name = request.GET.get('street_name')
    street_descriptor = request.GET.get('street_descriptor')

    if street_number:
        street_number = int(street_number)

    css_casses = CSSCase.objects.filter()
    for case in css_casses:
        results += filter_location_data(case, street_number, street_name, street_descriptor)

    pd_casses = PDCase.objects.filter()
    for case in pd_casses:
        results += filter_location_data(case, street_number, street_name, street_descriptor)

    return JsonResponse({
        'street_number': street_number,
        'street_name': street_name,
        'street_descriptor': street_descriptor,
        'data': results
    })

@login_required
def locations_data(request):
    results = {}

    css_cases = CSSCase.objects.filter()
    pd_cases = PDCase.objects.filter()

    for case in list(chain(pd_cases, css_cases)):
        normalized = normalize_address_string(case.raw_address)
        if normalized:
            combined = string.capwords(combine_address_parts(normalized[0], normalized[1]))
            if combined not in results:
                results[combined] = 0
            results[combined] += 1

    return JsonResponse({
        'results': sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)
    })

@login_required
def locations_view(request):

    return render(request, 'workflow/locations.html')

