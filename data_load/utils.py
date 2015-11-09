import json
import logging
import traceback
from datetime import datetime

import pytz

from data_load.models import RMSCase, CRWCase

log = logging.getLogger('consolelogger')


def get_latest_rms_case_no_util():
    latest_case_no = 11400000

    result = list(RMSCase.objects.raw("SELECT id, case_no FROM data_load_rmscase ORDER BY case_no DESC LIMIT 1"))

    if result:
        latest_case_no = result[0].case_no

    return latest_case_no


def get_latest_crw_case_no_util():
    latest_case_no = 'CE14-0000'

    result = list(CRWCase.objects.raw("SELECT id, case_no FROM data_load_crwcase ORDER BY case_no DESC LIMIT 1"))

    if result:
        latest_case_no = result[0].case_no

    return latest_case_no


def load_rms_cases(cases_json):
    cases = json.loads(cases_json)
    tz = pytz.timezone('America/Los_Angeles')

    added = 0
    skipped = 0
    for case in cases:
        date = case[1]
        date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

        try:
            RMSCase.objects.get_or_create(
                case_no=case[0],
                date=date_converted,
                code=case[2],
                desc=case[3],
                incnum=case[4] or None,
                address=case[5],
                off_name=case[7]
            )
            added += 1

        except:
            log.error("Error adding RMS case: {} - {}".format(str(case), traceback.format_exc()))
            skipped += 1

    return added, skipped


def load_crw_cases(cases_json):
    cases = json.loads(cases_json)
    tz = pytz.timezone('America/Los_Angeles')

    added = 0
    skipped = 0
    for case in cases:
        date = case[5]
        date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

        try:
            CRWCase.objects.create(
                yr_no=case[1],
                seq_no=case[2],
                started=date_converted,
                case_no=case[3],
                desc=case[4],
                case_type=case[6],
                case_subtype=case[7],
                address_number=case[8] or None,
                street_name=case[9],
                assigned_to=case[10],
                status=case[11]
            )
            added += 1

        except:
            log.error("Error adding CRW case: {} - {}".format(str(case), traceback.format_exc()))
            skipped += 1

    return added, skipped
