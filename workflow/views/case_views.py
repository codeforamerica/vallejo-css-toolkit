# import traceback
# import logging
# from django.db import connection
# from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def cases_data(request):
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
