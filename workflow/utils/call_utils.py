import re

from psycopg2.extensions import AsIs

from django.db import connection

from common.utils import dictfetchall
from intake.models import CallAuditItem, STATUS_CHOICES
from workflow.sql import CALLS_DATA_SQL, TOTAL_CALLS_COUNT_SQL


def get_calls_data(request_dict):
    idx_column_map = ['call_time', 'caller_name', 'caller_number', 'problem_address', 'status', 'assignee', 'count']

    searchable_columns = []
    search = None
    offset = 0
    limit = 10
    sort_by = 1
    sort_dir = 'asc'

    for k, v in request_dict.iteritems():
        if k == 'start' and v.isdigit():
            offset = int(v)

        if k == 'length' and v.isdigit():
            limit = int(v)

        if k == 'order[0][column]' and v.isdigit():
            sort_by = int(v) + 1  # psql column indicies start at 1

        if k == 'order[0][dir]' and v in ('asc', 'desc'):
            sort_dir = v

        if k == 'search[value]':
            search = v

        r = re.match('columns\[(?P<idx>\d+)\]\[searchable\]', k)
        if r and v == 'true':
            searchable_idx = r.groupdict()['idx']
            searchable_columns.append(idx_column_map[int(searchable_idx)])

    search_string = ''
    if search:
        search_cols_modified = [" {} ilike '%{}%' ".format(searchable_column, search) for searchable_column in searchable_columns]
        search_string = "WHERE {}".format(' OR '.join(search_cols_modified))

    cursor = connection.cursor()
    cursor.execute(CALLS_DATA_SQL, [AsIs(search_string), sort_by, AsIs(sort_dir), offset, limit])
    
    data_results = cursor.fetchall()
    if data_results:
        records_filtered = data_results[0][-1]
    else:
        records_filtered = 0

    cursor.execute(TOTAL_CALLS_COUNT_SQL)
    count_results = dictfetchall(cursor)
    if count_results:
        records_total = count_results[0].get('records_total', 0)
    else:
        records_total = 0

    return {'data': data_results, 'recordsFiltered': records_filtered, 'recordsTotal': records_total}

def create_call_audit_items(new, old, user, call):
    for field, new_value in new.iteritems():
        old_value = old.get(field)

        # if field == 'assignee':
        #     if old_value:
        #         old_assignee = get_object_or_404(User, id=old_value)
        #         old_value = old_assignee.get_full_name()

        #     if new_value:    
        #         new_assignee = get_object_or_404(User, username=new_value)
        #         new_value = new_assignee.get_full_name()

        if field == 'status':
            for status_choice in STATUS_CHOICES:
                if old_value == status_choice[0]:
                    old_value = status_choice[1]
                if new_value == status_choice[0]:
                    new_value = status_choice[1]

        if (old_value or new_value) and old_value != new_value:
            CallAuditItem.objects.create(user=user, call=call, changed_field=field, old_value=old_value, new_value=new_value)
