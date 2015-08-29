# import traceback
# import logging
# from django.db import connection
# from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from common.datatables import get_datatables_data

@login_required(login_url='/admin/login/')
def cases_data(request):
    request_dict = dict(request.GET.items())
    idx_column_map = ['description', 'resolution', 'status_id', 'address_number', 'street_name']

    CSS_CASES_DATA_SQL = """
        select
            c.description,
            c.resolution,
            c.status_id,
            c.address_number,
            c.street_name,
            count(*) over(),
            100
        from
            workflow_csscase c
        limit 10;
    """

    try:
        results = get_datatables_data(request_dict, CSS_CASES_DATA_SQL, idx_column_map)
        print results
    except Exception:
        # messages.add()
        log.error('Error encountered fetching from database: {}'.format(traceback.format_exc()))
        results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}

    return JsonResponse(results)

@login_required(login_url='/admin/login/')
def cases(request):
    return render(request, 'workflow/cases.html')

@login_required(login_url='/admin/login/')
def visit_queue_data(request):
    results = {'data': [], 'recordsFiltered': 0, 'recordsTotal': 0}
    return JsonResponse(results)

@login_required(login_url='/admin/login/')
def visit_queue(request):
    return render(request, 'workflow/visit_queue.html')
