import math
import logging
import traceback

from psycopg2.extensions import AsIs

from django.db import connection

log = logging.getLogger('consolelogger')


def get_location_history(address_number, street_name, report_id):
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
            UNION
            SELECT
                report.reported_datetime AT TIME ZONE 'America/Los_Angeles' AS date,
                'CSS' AS source,
                CAST(report.id AS TEXT) AS case_no,
                CASE WHEN report.report_type = 1 THEN 'Squatters'
                     WHEN report.report_type = 2 THEN 'Homeless encampment'
                     WHEN report.report_type = 3 THEN 'Drugs'
                     WHEN report.report_type = 4 THEN 'Illegal Auto Repair'
                     WHEN report.report_type = 5 THEN 'Illegal Dumping'
                     WHEN report.report_type = 6 THEN 'Prostitution'
                     WHEN report.report_type = 7 THEN 'Abandoned Vehicle'
                     WHEN report.report_type = 8 THEN 'Communication/Question'
                     WHEN report.report_type = 9 THEN 'Other'
                END AS case_type,
                report.problem AS description
            FROM workflow_csscall report
            WHERE report.address_number = %(address_number)s
            AND LOWER(report.street_name) = LOWER(%(street_name)s)
            AND report.id != %(report_id)s
        ) AS data
        ORDER BY data.date DESC
    """
    params = {'address_number': address_number, 'street_name': street_name, 'report_id': report_id}
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception:
        log.error("Encountered error fetching location history from the database: {}".format(traceback.format_exc()))
        raise
    finally:
        cursor.close()


def get_reports(request_params):
    sortable_fields = ['reported_datetime', 'reporter_name', 'problem_address', 'problem', 'status']
    searchable_fields = ['reported_datetime_str', 'reporter_name', 'problem_address', 'problem', 'status_str', 'id']
    default_limit = 25
    max_limit = 100
    default_offset = 0
    default_sort_key = 'reported_datetime'
    default_sort_order = 'DESC'

    search_get_param = request_params.get('search') and request_params['search'].strip()
    search_clause = ''
    if search_get_param:
        search_clause = "WHERE {} ".format("OR".join([" {} ilike '%{}%' ".format(field, search_get_param) for field in searchable_fields]))

    sort_key_get_param = request_params.get('sort_key')
    if sort_key_get_param:
        if sort_key_get_param in sortable_fields:
            sort_key = sort_key_get_param
        else:
            log.warning('Unexpected get query param for reports sort: {}, falling back to default sort key'.format(sort_key_get_param))
            sort_key = default_sort_key
    else:
        sort_key = default_sort_key

    sort_order_get_param = request_params.get('sort_order')
    if sort_order_get_param and sort_order_get_param.lower() == 'asc':
        sort_order = 'ASC'
    else:
        sort_order = default_sort_order

    offset_get_param = request_params.get('offset')
    if offset_get_param:
        if type(offset_get_param) in (str, unicode) and offset_get_param.isdigit():
            offset = int(offset_get_param)
        elif type(offset_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports offset: {} of type {}, falling back to default offset'.format(offset_get_param, type(offset_get_param)))
            offset = default_offset
    else:
        offset = default_offset

    limit_get_param = request_params.get('limit')
    if limit_get_param:
        if type(limit_get_param) in (str, unicode) and limit_get_param.isdigit():
            limit_get_param = int(limit_get_param)
        elif type(limit_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports limit: {} of type {}, falling back to default limit'.format(limit_get_param, type(limit_get_param)))
            limit = default_limit
        limit = min(limit_get_param, max_limit)
    else:
        limit = default_limit

    query = """
        WITH data AS (
            SELECT
                c.id::text AS id,
                c.reported_datetime AS reported_datetime,
                COALESCE(
                    TO_CHAR(
                        c.reported_datetime AT TIME ZONE 'America/Los_Angeles', 'MM/DD/YY HH24:MI'
                    )
                , '') AS reported_datetime_str,
                COALESCE(c.name, '') AS reporter_name,
                COALESCE(c.address, '') AS problem_address,
                COALESCE(c.problem, '') AS problem,
                c.status AS status,
                CASE WHEN c.status = 1 THEN 'Unread - phone'
                     WHEN c.status = 2 THEN 'Unread - web'
                     WHEN c.status = 3 THEN 'Report'
                     WHEN c.status = 4 THEN 'Verification'
                     WHEN c.status = 5 THEN 'Case'
                     WHEN c.status = 6 THEN 'Resolved'
                     ELSE ''
                END AS status_str
            FROM workflow_csscall AS c
            WHERE c.active = True
        ), total_count AS (
            SELECT COUNT(*) AS tcount FROM workflow_csscall
            WHERE active = True
        )
        SELECT
            data.id,
            data.reported_datetime_str,
            data.problem_address,
            data.reporter_name,
            data.problem,
            data.status,
            data.status_str,
            COUNT(*) OVER(),
            total_count.tcount
        FROM data, total_count
        %(search_clause)s
        ORDER BY %(sort_key)s %(sort_order)s, id
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    params = {
        'sort_key': AsIs(sort_key),
        'sort_order': AsIs(sort_order),
        'search_clause': AsIs(search_clause),
        'offset': offset,
        'limit': limit
    }
    cursor = connection.cursor()

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

        return results, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset
    except Exception:
        log.error("Encountered error fetching results from the database and building pagination: {}".format(traceback.format_exc()))
        raise
    finally:
        cursor.close()


def get_cases(request_params):
    sortable_fields = ['started', 'address', 'priority', 'description', 'status']
    searchable_fields = ['started_str', 'address', 'priority_str', 'description', 'status', 'id']
    default_limit = 25
    max_limit = 100
    default_offset = 0
    default_sort_key = 'started'
    default_sort_order = 'DESC'

    search_get_param = request_params.get('search') and request_params['search'].strip()
    search_clause = ''
    if search_get_param:
        search_clause = "WHERE {} ".format("OR".join([" {} ilike '%{}%' ".format(field, search_get_param) for field in searchable_fields]))
    print search_clause

    sort_key_get_param = request_params.get('sort_key')
    if sort_key_get_param:
        if sort_key_get_param in sortable_fields:
            sort_key = sort_key_get_param
        else:
            log.warning('Unexpected get query param for reports sort: {}, falling back to default sort key'.format(sort_key_get_param))
            sort_key = default_sort_key
    else:
        sort_key = default_sort_key

    sort_order_get_param = request_params.get('sort_order')
    if sort_order_get_param and sort_order_get_param.lower() == 'asc':
        sort_order = 'ASC'
    else:
        sort_order = default_sort_order

    offset_get_param = request_params.get('offset')
    if offset_get_param:
        if type(offset_get_param) in (str, unicode) and offset_get_param.isdigit():
            offset = int(offset_get_param)
        elif type(offset_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports offset: {} of type {}, falling back to default offset'.format(offset_get_param, type(offset_get_param)))
            offset = default_offset
    else:
        offset = default_offset

    limit_get_param = request_params.get('limit')
    if limit_get_param:
        if type(limit_get_param) in (str, unicode) and limit_get_param.isdigit():
            limit_get_param = int(limit_get_param)
        elif type(limit_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports limit: {} of type {}, falling back to default limit'.format(limit_get_param, type(limit_get_param)))
            limit = default_limit
        limit = min(limit_get_param, max_limit)
    else:
        limit = default_limit

    query = """
        WITH data AS (
            SELECT
                c.id::text AS id,
                c.created_at AS started,
                COALESCE(
                    TO_CHAR(
                        c.created_at AT TIME ZONE 'America/Los_Angeles', 'MM/DD/YY HH24:MI'
                    )
                , '') AS started_str,
                COALESCE(r.address_number::text || ' ' || r.street_name, '') AS address,
                c.priority AS priority,
                CASE WHEN c.priority = 1 THEN 'Low'
                     WHEN c.priority = 2 THEN 'Med'
                     WHEN c.priority = 3 THEN 'High'
                     ELSE ''
                END AS priority_str,
                COALESCE(r.problem, '') AS description,
                CASE WHEN r.status = 1 THEN 'Unread - phone'
                     WHEN r.status = 2 THEN 'Unread - web'
                     WHEN r.status = 3 THEN 'Report'
                     WHEN r.status = 4 THEN 'Verification'
                     WHEN r.status = 5 THEN 'Case'
                     WHEN r.status = 6 THEN 'Resolved'
                     ELSE ''
                END AS status
            FROM workflow_csscase AS c
            LEFT JOIN workflow_verification v
                ON c.verification_id = v.id
            LEFT JOIN workflow_csscall r
                ON v.report_id = r.id
            WHERE c.active = True
        ), total_count AS (
            SELECT COUNT(*) AS tcount FROM workflow_csscase
            WHERE active = True
        )
        SELECT
            data.id,
            data.started,
            data.started_str,
            data.address,
            data.priority,
            data.priority_str,
            data.description,
            data.status,
            COUNT(*) OVER(),
            total_count.tcount
        FROM data, total_count
        %(search_clause)s
        ORDER BY %(sort_key)s %(sort_order)s, id
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    params = {
        'sort_key': AsIs(sort_key),
        'sort_order': AsIs(sort_order),
        'search_clause': AsIs(search_clause),
        'offset': offset,
        'limit': limit
    }
    cursor = connection.cursor()

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

        return results, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset
    except Exception:
        log.error("Encountered error fetching results from the database and building pagination: {}".format(traceback.format_exc()))
        raise
    finally:
        cursor.close()


def get_properties(request_params):
    sortable_fields = ['address', 'num_incidents', 'latest_activity', 'status']
    searchable_fields = ['address', 'latest_activity_str']  # TODO: need to escape `status` as a protected psql var name?
    default_limit = 25
    max_limit = 100
    default_offset = 0
    default_sort_key = 'num_incidents'
    default_sort_order = 'DESC'

    search_get_param = request_params.get('search') and request_params['search'].strip()
    search_clause = ''
    if search_get_param:
        search_clause = "WHERE {} ".format("OR".join([" {} ilike '%{}%' ".format(field, search_get_param) for field in searchable_fields]))
    print search_clause

    sort_key_get_param = request_params.get('sort_key')
    if sort_key_get_param:
        if sort_key_get_param in sortable_fields:
            sort_key = sort_key_get_param
        else:
            log.warning('Unexpected get query param for reports sort: {}, falling back to default sort key'.format(sort_key_get_param))
            sort_key = default_sort_key
    else:
        sort_key = default_sort_key

    sort_order_get_param = request_params.get('sort_order')
    if sort_order_get_param and sort_order_get_param.lower() == 'asc':
        sort_order = 'ASC'
    else:
        sort_order = default_sort_order

    offset_get_param = request_params.get('offset')
    if offset_get_param:
        if type(offset_get_param) in (str, unicode) and offset_get_param.isdigit():
            offset = int(offset_get_param)
        elif type(offset_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports offset: {} of type {}, falling back to default offset'.format(offset_get_param, type(offset_get_param)))
            offset = default_offset
    else:
        offset = default_offset

    limit_get_param = request_params.get('limit')
    if limit_get_param:
        if type(limit_get_param) in (str, unicode) and limit_get_param.isdigit():
            limit_get_param = int(limit_get_param)
        elif type(limit_get_param) == int:
            pass
        else:
            log.warning('Unexpected get query param for reports limit: {} of type {}, falling back to default limit'.format(limit_get_param, type(limit_get_param)))
            limit = default_limit
        limit = min(limit_get_param, max_limit)
    else:
        limit = default_limit

    query = """
        WITH data AS (

            SELECT
                COALESCE(subselect.address, '') AS address,
                count(*) AS num_incidents,
                max(subselect.max_timestamp) AS latest_activity,
                COALESCE(
                    TO_CHAR(
                        max(subselect.max_timestamp) AT TIME ZONE 'America/Los_Angeles', 'MM/DD/YY HH24:MI'
                    )
                , '') AS latest_activity_str,
                'Report' AS status

            FROM (
                SELECT
                    COALESCE(r.address_number::text || ' ' || r.street_name, r.address, '') AS address,
                    latest_activities.max_timestamp as max_timestamp

                    FROM workflow_csscall r
                    LEFT JOIN
                    (
                        SELECT r.id as report_id, r.reported_datetime as max_timestamp

                        FROM workflow_csscall r

                        LEFT JOIN workflow_verification v
                            ON v.report_id = r.id
                        LEFT JOIN workflow_csscase c
                            ON c.verification_id = v.id

                        GROUP BY r.id

                    ) AS latest_activities
                    ON r.id = latest_activities.report_id

                WHERE COALESCE(r.address_number::text || ' ' || r.street_name, r.address) IS NOT NULL
                AND COALESCE(r.address_number::text || ' ' || r.street_name, r.address) != ''
                AND r.active = True
            ) as subselect

            GROUP BY address

        )
        SELECT
            data.address,
            data.num_incidents,
            data.latest_activity,
            data.latest_activity_str,
            data.status,
            COUNT(*) OVER()
        FROM data
        %(search_clause)s
        ORDER BY %(sort_key)s %(sort_order)s
        OFFSET %(offset)s
        LIMIT %(limit)s
    """

    params = {
        'sort_key': AsIs(sort_key),
        'sort_order': AsIs(sort_order),
        'search_clause': AsIs(search_clause),
        'offset': offset,
        'limit': limit
    }
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()

        pagination_keys = None
        page_idx = None
        if results:
            num_results = results[0][-1]
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

        return results, pagination_keys, page_idx, sort_key, search_get_param, sort_order, limit, offset
    except Exception:
        log.error("Encountered error fetching results from the database and building pagination: {}".format(traceback.format_exc()))
        raise
    finally:
        cursor.close()
