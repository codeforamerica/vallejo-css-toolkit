import logging
import traceback

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from data_load.utils import load_rms_cases, load_crw_cases, get_latest_crw_case_nos_util, get_latest_rms_case_no_util

log = logging.getLogger('consolelogger')


@csrf_exempt
def get_latest_rms_case_no(request):
    log.info('fetching latest rms case num')
    latest_case_no = get_latest_rms_case_no_util()

    return JsonResponse({'latest_case_no': latest_case_no})


@csrf_exempt
def get_latest_crw_case_nos(request):
    log.info('fetching latest crw case nums')
    latest_yr_no, latest_seq_no = get_latest_crw_case_nos_util()

    return JsonResponse({'latest_yr_no': latest_yr_no, 'latest_seq_no': latest_seq_no})


@csrf_exempt
def handle_rms_post(request):
    try:
        added, skipped = load_rms_cases(request.body)
        log.info('added {} new and skipped {} rms cases'.format(added, skipped))

        return JsonResponse({'status': 'OK'})

    except:
        log.error('Encountered error while adding new RMS cases: {}'.format(traceback.format_exc()))
        return JsonResponse({'error_traceback': traceback.format_exc()})


@csrf_exempt
def handle_crw_post(request):
    try:
        added, skipped = load_crw_cases(request.body)
        log.info('added {} new and skipped {} crw cases'.format(added, skipped))

        return JsonResponse({'status': 'OK'})

    except:
        log.error('Encountered error while adding new CRW cases: {}'.format(traceback.format_exc()))

        return JsonResponse({'error_traceback': traceback.format_exc()})
