import json
from datetime import datetime

import pytz

from data_load.models import RMSCase, CRWCase


def get_latest_rms_case_no_util():
    latest_case_no = 0

    result = list(RMSCase.objects.raw("SELECT id, case_no FROM data_load_rmscase ORDER BY case_no DESC LIMIT 1"))

    if result:
        latest_case_no = result[0].case_no

    return latest_case_no


def get_latest_crw_case_nos_util():
    latest_yr_no = 14
    latest_seq_no = 0

    result = list(CRWCase.objects.raw("SELECT id, yr_no, seq_no FROM data_load_crwcase ORDER BY yr_no, seq_no DESC LIMIT 1"))

    if result:
        latest_yr_no = result[0].yr_no
        latest_seq_no = result[0].seq_no

    return latest_yr_no, latest_seq_no


def load_rms_cases(cases_json):
    cases = json.loads(cases_json)
    tz = pytz.timezone('America/Los_Angeles')

    added = 0
    for case in cases:
        date = case[1]
        date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

        rms_case, _ = RMSCase.objects.get_or_create(case_no=case[0])
        rms_case.date = date_converted
        rms_case.code = case[2]
        rms_case.desc = case[3]
        rms_case.incnum = case[4]
        rms_case.address = case[5]
        rms_case.off_name = case[7]
        rms_case.save()
        added += 1

    return added


def load_crw_cases(cases_json):
    cases = json.loads(cases_json)
    tz = pytz.timezone('America/Los_Angeles')

    added = 0
    for case in cases:
        date = case[5]
        date_converted = tz.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

        crw_case, _ = CRWCase.objects.get_or_create(yr_no=case[1], seq_no=case[2])
        crw_case.started = date_converted
        crw_case.case_no = case[3]
        crw_case.desc = case[4]
        crw_case.case_type = case[6]
        crw_case.case_subtype = case[7]
        crw_case.address_number = case[8]
        crw_case.street_name = case[9]
        crw_case.assigned_to = case[10]
        crw_case.status = case[11]
        crw_case.save()
        added += 1

    return added
