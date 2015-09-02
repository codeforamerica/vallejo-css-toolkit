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
        # normalized = normalize_address_string(case.raw_address)
        # if not normalized:
        #     log.info('NORMALIZER_MISS: {}'.format(case.raw_address))
        #     continue

        # street_number, street_name, street_descriptor = normalized
        # coords = geocode(street_number, street_name, street_descriptor)
        coords = geocode(case.address_number, case.street_name)
        if coords:
            results.append({'lat': coords['lat'], 'lng': coords['lng']})
        else:
            log.info('GEOCODE_MISS - {}|{}'.format(case.address_number, case.street_name))

    return JsonResponse({'results': results})

@login_required(login_url='/admin/login/')
def css_data(request):
    cases = CSSCase.objects.filter()
    return process_case_data(cases)

@login_required(login_url='/admin/login/')
def rms_data(request):
    cases = PDCase.objects.filter()[:1000]
    return process_case_data(cases)

@login_required(login_url='/admin/login/')
def map_view(request):

    return render(request, 'workflow/map.html')

def filter_location_data(case, address_number, street_name):
    # normalized = normalize_address_string(case.raw_address)
    if case.address_number == address_number and case.street_name == street_name:
        return [case.id]
    return []

@login_required(login_url='/admin/login/')
def location_data(request):
    results = []

    address_number = request.GET.get('address_number')
    street_name = request.GET.get('street_name')

    if address_number:
        street_number = int(address_number)

    css_casses = CSSCase.objects.filter()
    for case in css_casses:
        results += filter_location_data(case, address_number, street_name)

    pd_casses = PDCase.objects.filter()
    for case in pd_casses:
        results += filter_location_data(case, address_number, street_name)

    return JsonResponse({
        'address_number': address_number,
        'street_name': street_name,
        'data': results
    })

@login_required(login_url='/admin/login/')
def locations_data(request):
    results = {}

    css_cases = CSSCase.objects.filter()
    pd_cases = PDCase.objects.filter()

    for case in list(chain(pd_cases, css_cases)):
        # normalized = normalize_address_string(case.raw_address)
        # if normalized:
        #     combined = string.capwords(combine_address_parts(normalized[0], normalized[1]))
        combined = "{} {}".format(case.address_number, case.street_name)
        if combined not in results:
            results[combined] = 0
        results[combined] += 1

    return JsonResponse({
        'results': sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)
    })
