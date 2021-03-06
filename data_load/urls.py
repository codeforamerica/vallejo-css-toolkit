from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # endpoint for ETL process to check crw high water mark
    url(r'^get_latest_crw_case_no/$', 'data_load.views.get_latest_crw_case_no', name='get_latest_crw_case_no'),

    # endpoint for ETL process to check rms high water mark
    url(r'^get_latest_rms_case_no/$', 'data_load.views.get_latest_rms_case_no', name='get_latest_rms_case_no'),

    # endpoint for ETL process to check rms high water mark
    url(r'^get_latest_rms_incident_no/$', 'data_load.views.get_latest_rms_incident_no', name='get_latest_rms_incident_no'),

    # endpoint for ETL process to post crw updates
    url(r'^handle_crw_post/$', 'data_load.views.handle_crw_post', name='handle_crw_post'),

    # endpoint for ETL process to post rms case updates
    url(r'^handle_rms_post/$', 'data_load.views.handle_rms_post', name='handle_rms_post'),

    # endpoint for ETL process to post rms incident updates
    url(r'^handle_rms_inc_post/$', 'data_load.views.handle_rms_inc_post', name='handle_rms_inc_post'),

)
