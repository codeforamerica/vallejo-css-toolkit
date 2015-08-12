from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^intake/welcome/$', 'intake.views.welcome', name='welcome'),
    url(r'^intake/handle-name/', 'intake.views.handle_name', name='handle_name'),
    url(r'^intake/handle-name-transcription/', 'intake.views.handle_name_transcription', name='handle_name_transcription'),
    url(r'^intake/handle-feedback-pref/', 'intake.views.handle_feedback_pref', name='handle_feedback_pref'),
    url(r'^intake/handle-feedback-number/', 'intake.views.handle_feedback_number', name='handle_feedback_number'),
    url(r'^intake/handle-problem-address/', 'intake.views.handle_problem_address', name='handle_problem_address'),
    url(r'^intake/handle-problem-address-transcription/', 'intake.views.handle_problem_address_transcription', name='handle_problem_address_transcription'),
    url(r'^intake/handle-problem-description/', 'intake.views.handle_problem_description', name='handle_problem_description'),
    url(r'^intake/handle-problem-description-transcription/', 'intake.views.handle_problem_description_transcription', name='handle_problem_description_transcription'),
    url(r'^intake/call/(?P<call_id>\d*)/$', 'intake.views.call', name='call'),
    url(r'^intake/audit_log/$', 'intake.views.audit_log', name='audit_log'),
    url(r'^intake/audit_log_data/$', 'intake.views.audit_log_data', name='audit_log_data'),
    url(r'^intake/my_assignments/$', 'intake.views.assigned_to_current_user', name='assigned_to_current_user'),
    url(r'^intake/my_assignments_data/$', 'intake.views.assigned_to_current_user_data', name='assigned_to_current_user_data'),
    url(r'^sms_reply/$', 'intake.views.sms_reply', name='sms_reply'),
    url(r'^workflow/map/$', 'workflow.views.map_view', name='map_view'),
    url(r'^workflow/css_data/$', 'workflow.views.css_data', name='css_data'),
    url(r'^workflow/rms_data/$', 'workflow.views.rms_data', name='rms_data'),
    url(r'^workflow/location_data/$', 'workflow.views.location_data', name='lcoation_data'),
    url(r'^workflow/locations_data/$', 'workflow.views.locations_data', name='lcoations_data'),
)

