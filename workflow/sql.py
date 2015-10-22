AUDIT_LOG_IDX_COLUMN_MAP = [
    'call_time',
    'timestamp',
    'name',
    'changed_field',
    'old_value',
    'new_value',
    'count',
    'tcount'
]

AUDIT_LOG_DATA_SQL = """
    SET TIME ZONE 'America/Los_Angeles';

    WITH data AS (
        SELECT
            COALESCE('<a href="/workflow/call/' || c.id || '">' || TO_CHAR(c.call_time, 'YYYY-MM-DD HH24:MI') || '</a>', '') AS call_time,
            COALESCE(to_char(cai.timestamp, 'MM-DD-YYYY HH24:MI'), '') AS timestamp,
            COALESCE(u.first_name::VARCHAR || ' ', '') || COALESCE(u.last_name, '') AS name,
            REPLACE(COALESCE(cai.changed_field, ''), '_', ' ') AS changed_field,
            COALESCE(cai.old_value, '') AS old_value,
            COALESCE(cai.new_value, '') AS new_value
        FROM intake_call c
        JOIN intake_callaudititem cai
            ON c.id = cai.call_id
        LEFT JOIN auth_user u
            ON cai.user_id = u.id
    ), total_count AS (
        SELECT COUNT(*) AS tcount FROM intake_callaudititem
    )
    SELECT
        data.call_time,
        data.timestamp,
        data.name,
        data.changed_field,
        data.old_value,
        data.new_value,
        COUNT(*) OVER(),
        total_count.tcount
    FROM data, total_count
    %s
    ORDER BY %s %s
    OFFSET %s
    LIMIT %s
    ;
    """

CALLS_IDX_COLUMN_MAP = [
    'id',
    'reported_datetime',
    'reported_datetime_link',
    'caller_name',
    'caller_name_link'
    'caller_number',
    'caller_number_link',
    'problem_address',
    'problem_address_link',
    'status',
    'status_link',
    'resolution',
    'resolution_link',
    'count',
    'tcount'
]

CALLS_DATA_SQL = """
    WITH data AS (
        SELECT
            c.id AS id,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.reported_datetime AT TIME ZONE 'America/Los_Angeles'  || '</a>', '') AS reported_datetime_link,
            c.reported_datetime AT TIME ZONE 'America/Los_Angeles' AS reported_datetime,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.name  || '</a>', '') AS caller_name_link,
            c.name AS caller_name,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.phone  || '</a>', '') AS caller_number_link,
            c.phone AS caller_number,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.address  || '</a>', '') AS problem_address_link,
            c.address AS problem_address,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.problem  || '</a>', '') AS status_link,
            c.problem AS status,

            COALESCE('<a href="/workflow/report/' || c.id || '">' || c.resolution  || '</a>', '') AS resolution_link,
            c.resolution AS resolution

        FROM workflow_csscall as c
    ), total_count AS (
        SELECT COUNT(*) as tcount FROM workflow_csscall
    )
    SELECT
        data.id,

        data.reported_datetime,
        data.reported_datetime_link,

        data.caller_name,
        data.caller_name_link,

        data.caller_number,
        data.caller_number_link,

        data.problem_address,
        data.problem_address_link,

        data.status,
        data.status_link,

        data.resolution,
        data.resolution_link,

        COUNT(*) OVER(),
        total_count.tcount

    FROM data, total_count
    %s
    ORDER BY %s %s
    OFFSET %s
    LIMIT %s
    ;
    """

CSS_CASES_IDX_COLUMN_MAP = [
    'address',
    'id',
    'description',
    'resolution',
    'status_id',
    'full_address',
    'count',
    'tcount'
]

CSS_CASES_DATA_SQL = """
    WITH data AS (
        SELECT
            c.id as raw_id,
            c.address_number || '&nbsp' || c.street_name AS full_address,
            c.description,
            c.resolution,
            c.status_id,
            count(*) over()
        FROM workflow_csscase c
    ), total_count AS (
        SELECT COUNT(*) AS tcount FROM workflow_csscase
    )
    SELECT
        '<a href="/workflow/case/' || data.raw_id || '">' || data.full_address || '</a>'AS address,
        data.raw_id as id,
        data.description as description,
        data.resolution as resolution,
        data.status_id as status_id,
        data.full_address as full_address,
        COUNT(*) OVER(),
        total_count.tcount
    FROM
        data, total_count
    %s
    ORDER BY %s %s
    OFFSET %s
    LIMIT %s
    ;
    """
