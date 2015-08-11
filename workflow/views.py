from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse

from geo.models import Location

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
        SELECT lat, lng
        from workflow_csscase
        where
            lat is not null
            and lng is not null
            and dept is null
        ;"""
    )

    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def rms_data(request):

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT lat, lng
        from workflow_pdcase
        where
            lat is not null
            and lng is not null
            and dept = 1
        ;"""
    )

    results = dictfetchall(cursor)

    return JsonResponse({'results': results})

@login_required
def map_view(request):

    return render(request, 'workflow/map.html')

@login_required
def location_view(request, location_id):
    instance = get_object_or_404(Location, id=location_id)

    return render(request, 'workflow/location.html', {'location': instance})
