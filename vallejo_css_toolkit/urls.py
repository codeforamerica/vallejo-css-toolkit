from django.contrib import admin
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    # new call in related urls
    url(r'^intake/step-one/$', 'intake.views.step_one', name='step_one'),
    url(r'^intake/step-two/$', 'intake.views.step_two', name='step_two'),
    url(r'^intake/step-three/$', 'intake.views.step_three', name='step_three'),
    url(r'^intake/step-four/$', 'intake.views.step_four', name='step_four'),
    url(r'^intake/step-five/$', 'intake.views.step_five', name='step_five'),
    url(r'^intake/step-six/$', 'intake.views.step_six', name='step_six'),
    url(r'^intake/step-seven/$', 'intake.views.step_seven', name='step_seven'),
    url(r'^intake/step-eight/$', 'intake.views.step_eight', name='step_eight'),
    url(r'^intake/step-nine/$', 'intake.views.step_nine', name='step_nine'),
    url(r'^intake/step-ten/$', 'intake.views.step_ten', name='step_ten'),
    url(r'^intake/step-eleven/$', 'intake.views.step_eleven', name='step_eleven'),
    url(r'^intake/step-twelve/$', 'intake.views.step_twelve', name='step_twelve'),
    url(r'^intake/step-thirteen/$', 'intake.views.step_thirteen', name='step_thirteen'),
    url(r'^intake/step-fourteen/$', 'intake.views.step_fourteen', name='step_fourteen'),

    # all call-in related urls
    url(r'^intake/welcome/$', 'intake.views.welcome', name='welcome'),
    url(r'^intake/handle-name/$', 'intake.views.handle_name', name='handle_name'),
    url(r'^intake/handle-name-transcription/$', 'intake.views.handle_name_transcription', name='handle_name_transcription'),
    url(r'^intake/handle-feedback-pref/$', 'intake.views.handle_feedback_pref', name='handle_feedback_pref'),
    url(r'^intake/handle-feedback-number/$', 'intake.views.handle_feedback_number', name='handle_feedback_number'),
    url(r'^intake/handle-problem-address/$', 'intake.views.handle_problem_address', name='handle_problem_address'),
    url(r'^intake/handle-problem-address-transcription/$', 'intake.views.handle_problem_address_transcription', name='handle_problem_address_transcription'),
    url(r'^intake/handle-problem-description/$', 'intake.views.handle_problem_description', name='handle_problem_description'),
    url(r'^intake/handle-problem-description-transcription/$', 'intake.views.handle_problem_description_transcription', name='handle_problem_description_transcription'),

    # one-off for people to text in questions
    url(r'^sms_reply/$', 'intake.views.sms_reply', name='sms_reply'),

    # endpoint for zapier to post typeform submissions to
    url(r'^handle_typeform/$', 'intake.views.handle_typeform', name='handle_typeform'),

    # endpoint for ETL process to post crw updates
    url(r'^handle_crw_post/$', 'intake.views.handle_crw_post', name='handle_crw_post'),

    # endpoint for ETL process to post crw updates
    url(r'^handle_rms_post/$', 'intake.views.handle_rms_post', name='handle_rms_post'),

    # endpoint for ETL process to check high water mark
    url(r'^get_latest_case_no/$', 'intake.views.get_latest_case_no', name='get_latest_case_no'),

    # TODO: add case audit items to audit log

    # landing page view
    url(r'^$', 'workflow.views.landing', name='landing'),

    # call audit related views
    # url(r'^workflow/call_audit_log/$', 'workflow.views.call_views.call_audit_log', name='call_audit_log'),
    # url(r'^workflow/call_audit_log_data/$', 'workflow.views.call_views.call_audit_log_data', name='call_audit_log_data'),

    # case related views
    url(r'^workflow/case/(?P<case_id>\d*)/$', 'workflow.views.case_views.case', name='case'),
    url(r'^workflow/cases/$', 'workflow.views.case_views.cases', name='cases'),
    url(r'^workflow/cases_data/$', 'workflow.views.case_views.cases_data', name='cases_data'),
    url(r'^workflow/add_case_assignee/$', 'workflow.views.case_views.add_case_assignee', name='add_case_assignee'),
    url(r'^workflow/remove_case_assignee/$', 'workflow.views.case_views.remove_case_assignee', name='remove_case_assignee'),

    # verification related views
    url(r'^workflow/verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.verification', name='verfication'),

    # visit-queue related views
    url(r'^workflow/visit_queue/$', 'workflow.views.case_views.visit_queue', name='visit_queue'),
    url(r'^workflow/visit_queue_data/$', 'workflow.views.case_views.visit_queue_data', name='visit_queue_data'),

    # map-related views
    url(r'^workflow/map/$', 'workflow.views.location_views.map_view', name='map_view'),
    url(r'^workflow/css_data/$', 'workflow.views.location_views.css_data', name='css_data'),
    url(r'^workflow/rms_data/$', 'workflow.views.location_views.rms_data', name='rms_data'),

    # location-related views
    url(r'^workflow/location_data/$', 'workflow.views.location_views.location_data', name='lcoation_data'),
    url(r'^workflow/locations_data/$', 'workflow.views.location_views.locations_data', name='lcoations_data'),

    # report related views
    url(r'^workflow/report/(?P<report_id>\d*)/$', 'workflow.views.report_views.report', name='report'),
    url(r'^workflow/reports/$', 'workflow.views.report_views.reports', name='reports'),
    url(r'^workflow/reports_data/$', 'workflow.views.report_views.reports_data', name='reports_data'),
    url(r'^workflow/add_report/$', 'workflow.views.report_views.add_report', name='add_report'),

    # dataload-related views
    url(r'^data_load/import_csv/$', 'data_load.views.import_csv', name='import_csv'),

)
