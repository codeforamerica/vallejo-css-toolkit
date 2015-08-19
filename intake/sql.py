AUDIT_LOG_DATA_SQL = """
    SET TIME ZONE 'America/Los_Angeles';

    SELECT
        COALESCE(u.first_name, '') AS first_name,
        COALESCE(u.last_name, '') AS last_name,
        c.id,
        c.caller_number AS caller_number,
        COALESCE(to_char(cai.timestamp, 'MM-DD-YYYY HH24:MI:SS'), '') AS timestamp,
        REPLACE(COALESCE(cai.changed_field, ''), '_', ' ') AS changed_field,
        COALESCE(cai.old_value, '') AS old_value,
        COALESCE(cai.new_value, '') AS new_value
    FROM intake_call c
    JOIN intake_callaudititem cai
        ON c.id = cai.call_id
    LEFT JOIN auth_user u
        ON cai.user_id = u.id
    ORDER BY timestamp DESC;
    """

CURRENT_USER_ASSIGNMENTS_SQL = """
    SET TIME ZONE 'America/Los_Angeles';

    SELECT
        call_data.caller_number,
        call_data.id,
        call_data.call_time,
        call_data.caller_name,
        call_data.problem_address,
        call_data.status,
        update_data.last_updated
    FROM (
        SELECT
            c.id,
            c.caller_number AS caller_number,
            COALESCE(TO_CHAR(c.call_time, 'MM-DD-YYYY HH24:MI:SS'), '') AS call_time,
            COALESCE(c.caller_name, '') AS caller_name,
            COALESCE(c.problem_address, '') AS problem_address,
            c.status AS status
        FROM intake_call c
        WHERE assignee_id = %s
        ORDER BY c.call_time DESC
    ) call_data
    LEFT JOIN (
        SELECT
            COALESCE(TO_CHAR(MAX(cai.timestamp), 'MM-DD-YYYY HH24:MI:SS'), '') AS last_updated,
            cai.call_id AS call_id
        FROM intake_callaudititem cai
        GROUP BY cai.call_id
    ) update_data
    ON call_data.id = update_data.call_id;
    """

CALLS_DATA_SQL = """
    SET TIME ZONE 'America/Los_Angeles';

    WITH data AS (
        SELECT
            COALESCE('<a href="/intake/call/' || c.id || '">' || TO_CHAR(c.call_time, 'YYYY-MM-DD HH24:MI:SS') || '</a>', '') AS call_time,
            c.caller_name::VARCHAR AS caller_name,
            c.caller_number::VARCHAR AS caller_number,
            c.problem_address::VARCHAR AS problem_address,
            c.status::VARCHAR AS status,
            COALESCE(u.first_name::VARCHAR || ' ', '') || COALESCE(u.last_name, '') AS assignee
        FROM intake_call c
        LEFT JOIN auth_user u
        ON c.assignee_id = u.id
    )
    SELECT
        data.call_time,
        data.caller_name,
        data.caller_number,
        data.problem_address,
        data.status,
        data.assignee,
        COUNT(*) OVER()
    FROM data
    %s
    ORDER BY %s %s
    OFFSET %s
    LIMIT %s
    ;
    """

TOTAL_CALLS_COUNT_SQL = """
    SELECT COUNT(*) AS records_total FROM intake_call;
    """
