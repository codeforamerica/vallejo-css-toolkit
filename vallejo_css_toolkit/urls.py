from django.conf.urls import patterns, include, url
from django.contrib import admin

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

    # call audit related views
    url(r'^workflow/call_audit_log/$', 'workflow.views.call_views.call_audit_log', name='call_audit_log'),
    url(r'^workflow/call_audit_log_data/$', 'workflow.views.call_views.call_audit_log_data', name='call_audit_log_data'),

    # case audit related views
    # TODO:
    # url(r'^workflow/case/(?P<call_id>\d*)/$', 'workflow.views.case_views.case', name='case'),
    # url(r'^workflow/cases/$', 'workflow.views.case_views.cases', name='cases'),
    # url(r'^workflow/cases_data/$', 'workflow.views.case_views.cases_data', name='cases_data'),

    # my assigned calls -- TODO: not actively supported, change this to represent *cases* assigned to current user, or maybe search is fine
    url(r'^workflow/my_assignments/$', 'workflow.views.call_views.assigned_to_current_user', name='assigned_to_current_user'),
    url(r'^workflow/my_assignments_data/$', 'workflow.views.call_views.assigned_to_current_user_data', name='assigned_to_current_user_data'),

    # map-related views
    url(r'^workflow/map/$', 'workflow.views.location_views.map_view', name='map_view'),
    url(r'^workflow/css_data/$', 'workflow.views.location_views.css_data', name='css_data'),
    url(r'^workflow/rms_data/$', 'workflow.views.location_views.rms_data', name='rms_data'),

    # location-related views
    url(r'^workflow/location_data/$', 'workflow.views.location_views.location_data', name='lcoation_data'),
    url(r'^workflow/locations_data/$', 'workflow.views.location_views.locations_data', name='lcoations_data'),
    url(r'^workflow/locations/$', 'workflow.views.location_views.locations_view', name='lcoations_view'),

    # call admin-related views
    url(r'^workflow/call/(?P<call_id>\d*)/$', 'workflow.views.call_views.call', name='call'),
    url(r'^workflow/calls/$', 'workflow.views.call_views.calls', name='calls'),
    url(r'^workflow/calls_data/$', 'workflow.views.call_views.calls_data', name='calls_data'),

)
