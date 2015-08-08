import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse

from workflow.models import Case

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@login_required
def map_data(request):

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT lat, lng from workflow_case where lat is not null and lng is not null and dept is null;
        """
    )

    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def rms_data(request):

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT lat, lng from workflow_case where lat is not null and lng is not null and dept = 1;
        """
    )

    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def map_view(request):


    # TODO: move this template
    return render(request, 'intake/map.html')
