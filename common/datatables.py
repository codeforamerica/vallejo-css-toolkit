import re

from psycopg2.extensions import AsIs

from django.db import connection


def get_datatables_data(request_dict, sql_base_query, column_map):
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
            searchable_columns.append(column_map[int(searchable_idx)])

    search_string = ''
    if search:
        search_cols_modified = [" {} ilike '%{}%' ".format(searchable_column, search) for searchable_column in searchable_columns]
        search_string = "WHERE {}".format(' OR '.join(search_cols_modified))

    cursor = connection.cursor()
    try:
        cursor.execute(sql_base_query, [AsIs(search_string), sort_by, AsIs(sort_dir), offset, limit])
        data_results = cursor.fetchall()
    finally:
        cursor.close()

    if data_results:
        records_filtered = data_results[0][-2]
        records_total = data_results[0][-1]
    else:
        records_filtered = 0
        records_total = 0

    return {'data': data_results, 'recordsFiltered': records_filtered, 'recordsTotal': records_total}
