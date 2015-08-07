import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from workflow.models import Case

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

@login_required
def map_view(request):

    # placeholder for db call to fetch geocoded reports
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT lat, lng from workflow_case where lat is not null and lng is not null;
        """
    )

    results = dictfetchall(cursor)

    # TODO: move this template
    return render(request, 'intake/map.html', {'objs': json.dumps(results)})
