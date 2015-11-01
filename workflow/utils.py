import math
import logging

from psycopg2.extensions import AsIs

from django.db import connection

log = logging.getLogger('consolelogger')


def get_location_history(address_number, street_name):
    query = """
        SELECT TO_CHAR(data.date, 'MM/DD/YYYY'), data.source, data.case_no, data.case_type, data.description
        FROM (
            SELECT
                crw.started AT TIME ZONE 'America/Los_Angeles' AS date,
                'CRW' AS source,
                crw.case_no AS case_no,
                crw.case_subtype AS case_type,
                crw."desc" AS description
            FROM data_load_crwcase crw
            WHERE crw.address_number = %(address_number)s
            AND LOWER(crw.street_name) = LOWER(%(street_name)s)
            AND crw.started IS NOT NULL
            UNION
            SELECT
                rms.date AT TIME ZONE 'America/Los_Angeles' AS date,
                'RMS' AS source,
                CAST(rms.case_no AS TEXT) AS case_no,
                rms.code AS case_type,
                rms."desc" AS description
            FROM data_load_rmscase rms
            WHERE LOWER(rms.address) = CAST(%(address_number)s AS TEXT) || ' ' || LOWER(%(street_name)s)
            AND rms.date IS NOT NULL
        ) AS data
        ORDER BY data.date DESC
    """
    params = {'address_number': address_number, 'street_name': street_name}
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception:
        # TODO: log these
        raise
    finally:
        cursor.close()


def get_reports(request_params):
    sortable_fields = ['reported_datetime', 'reporter_name', 'problem_address', 'problem', 'notes']
    searchable_fields = ['reported_datetime', 'reporter_name', 'problem_address', 'problem', 'notes']
    default_limit = 25
    max_limit = 100
    default_offset = 0
    default_sort_key = 'reported_datetime'
    default_sort_order = 'DESC'

    search = request_params.get('search') and request_params['search'].strip()
    search_clause = ''
    if search:
        search_clause = "WHERE {} ".format("OR".join([" {} ilike '%{}%' ".format(field, search) for field in searchable_fields]))

    sort = request_params.get('sort')
    if sort:
        if sort[0] == '-':
            sort_order = 'DESC'
            sort_key = sort[1:]
        else:
            sort_key = sort
            sort_order = 'ASC'
    else:
        sort_key = default_sort_key
        sort_order = default_sort_order

    if sort_key not in sortable_fields:
        log.warning('Unexpected get query param for reports sort: {}, falling back to default sort key'.format(sort_key))
        sort_key = default_sort_key
        sort_order = default_sort_order

    offset = request_params.get('offset')
    if offset:
        if type(offset) in (str, unicode) and offset.isdigit():
            offset = int(offset)
        elif type(offset) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports offset: {} of type {}, falling back to default offset'.format(offset, type(offset)))
            offset = default_offset
    else:
        offset = default_offset

    limit = request_params.get('limit')
    if limit:
        if type(limit) in (str, unicode) and limit.isdigit():
            limit = int(limit)
        elif type(limit) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports limit: {} of type {}, falling back to default limit'.format(limit, type(limit)))
            limit = default_limit
        limit = min(limit, max_limit)
    else:
        limit = default_limit

    query = """
        WITH data AS (
            SELECT
                c.id AS id,
                COALESCE(TO_CHAR(c.reported_datetime AT TIME ZONE 'America/Los_Angeles', 'YYYY-MM-DD HH24:MI'), '') AS reported_datetime,
                c.name AS reporter_name,
                c.address AS problem_address,
                c.problem AS problem,
                c.resolution AS notes
            FROM workflow_csscall AS c
            WHERE c.active = True
        ), total_count AS (
            SELECT COUNT(*) AS tcount FROM workflow_csscall
            WHERE active = True
        )
        SELECT
            data.id,
            data.reported_datetime,
            data.reporter_name,
            data.problem_address,
            data.problem,
            data.notes,
            COUNT(*) OVER(),
            total_count.tcount
        FROM data, total_count
        %(search_clause)s
        ORDER BY %(sort_key)s %(sort_order)s
        NULLS LAST
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    params = {'sort_key': AsIs(sort_key), 'sort_order': AsIs(sort_order), 'search_clause': AsIs(search_clause), 'offset': offset, 'limit': limit}
    cursor = connection.cursor()

    base_url_parts = []
    if limit and limit != default_limit:
        base_url_parts.append("limit={}".format(limit))
    if sort_key and sort_key != default_sort_key and sort_order and sort_order != default_sort_order:
        base_url_parts.append("sort={}".format(sort))
    if search:
        base_url_parts.append("search={}".format(search))
    base_url_parts.append("offset=")

    base_url = base_url_parts and "?{}".format("&".join(base_url_parts)) or ""

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()

        pagination_keys = None
        page_idx = None
        if results:
            num_results = results[0][-2]
            num_pages = int(math.ceil(float(num_results) / limit))
            page_idx = offset // limit

            if num_pages <= 7:
                page_indices = range(1, num_pages + 1)
            else:
                if page_idx < 4:
                    page_indices = range(1, 6) + ['...'] + [num_pages]
                elif num_pages - page_idx < 5:
                    page_indices = [1, '...'] + range(num_pages - 4, num_pages + 1)
                else:
                    page_indices = [1, '...', page_idx, page_idx + 1, page_idx + 2, '...', num_pages]

            pagination_keys = [(i, (i - 1) * limit) if i != '...' else (i, None) for i in page_indices]

        current_url_params = "{}{}".format(base_url, offset)

        return results, pagination_keys, page_idx, base_url, current_url_params
    except Exception:
        # TODO: log these
        raise
    finally:
        cursor.close()
