from django.db import connection


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
