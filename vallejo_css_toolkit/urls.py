from django.contrib import admin
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # all call-in related urls
    url(r'^intake/welcome/$','intake.views.welcome',name='welcome'),
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

    # TODO: add case audit items to audit log

    # landing page view
    url(r'^$', 'workflow.views.landing', name='landing'),

    # call audit related views
    url(r'^workflow/call_audit_log/$', 'workflow.views.call_views.call_audit_log', name='call_audit_log'),
    url(r'^workflow/call_audit_log_data/$', 'workflow.views.call_views.call_audit_log_data', name='call_audit_log_data'),

    # case related views
    url(r'^workflow/case/(?P<case_id>\d*)/$', 'workflow.views.case_views.case', name='case'),
    url(r'^workflow/cases/$', 'workflow.views.case_views.cases', name='cases'),
    url(r'^workflow/cases_data/$', 'workflow.views.case_views.cases_data', name='cases_data'),
    url(r'^workflow/add_case_assignee/$', 'workflow.views.case_views.add_case_assignee', name='add_case_assignee'),
    url(r'^workflow/remove_case_assignee/$', 'workflow.views.case_views.remove_case_assignee', name='remove_case_assignee'),


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

    # call admin-related views
    url(r'^workflow/call/(?P<call_id>\d*)/$', 'workflow.views.call_views.call', name='call'),
    url(r'^workflow/calls/$', 'workflow.views.call_views.calls', name='calls'),
    url(r'^workflow/calls_data/$', 'workflow.views.call_views.calls_data', name='calls_data'),
    url(r'^workflow/add_call/$', 'workflow.views.call_views.add_call', name='add_call'),

    # dataload-related views
    url(r'^data_load/import_csv/$', 'data_load.views.import_csv', name='import_csv'),

)
