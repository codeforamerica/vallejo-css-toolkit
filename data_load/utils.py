import os
import sys 
import json

import requests
from requests.auth import HTTPDigestAuth


def scrape_realquest(address_number, street_name):

    data = {
        "address": "{} {}".format(address_number, street_name),
        "city": "Vallejo",
        "state_address": "CA",
        "action": "search",
        "avmcascadetype": "yes",
        "corevaluationdate": "09/16/2015",
        "detailproperty": "yes",
        "lp": "Address_Search",
        "maskSSNInput": "yes",
        "maskSSNInputOption": "fullmask",
        "searchpagesubmit": "Address_Search",
        "sl_sort": "None",
        "sorttype": "SORT",
        "type": "address",
        "valuationdate": "09/16/2015",
        "x": "73",
        "y": "20"
    }

    s = requests.Session()
    s.auth = HTTPDigestAuth('MC296275', os.environ.get('REALQUEST_PASS'))

    # r = s.post(
    #     url = "https://proclassic.realquest.com/jsp/rq.jsp?&client=",
    #     data = data,
    #     headers = {
    #         'content-type': 'application/x-www-form-urlencoded'
    #     }
    # )

    # print r.text.encode('utf-8')
    # print r.status_code

    requests.get('https://pro.realquest.com/home/?&client=&action=switch&page=main', auth=s.auth).text
    print requests.get('https://proclassic.realquest.com/jsp/rq.jsp?&client=&page=Address_Search&tab=ss&action=switch', auth=s.auth).text

if __name__ == "__main__":

    address_number = sys.argv[1]
    street_name = sys.argv[2]

    scrape_realquest(address_number, street_name)
