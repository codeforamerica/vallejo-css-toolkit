from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # case related views
    url(r'^workflow/case/(?P<case_id>\d*)/$', 'workflow.views.case_views.case', name='case'),
    url(r'^workflow/cases/$', 'workflow.views.case_views.cases', name='cases'),
    url(r'^workflow/add_case_assignee/$', 'workflow.views.case_views.add_case_assignee', name='add_case_assignee'),
    url(r'^workflow/remove_case_assignee/$', 'workflow.views.case_views.remove_case_assignee', name='remove_case_assignee'),
    url(r'^workflow/get_case_assignees/$', 'workflow.views.case_views.get_case_assignees', name='get_case_assignees'),
    url(r'^workflow/resolve_case/(?P<case_id>\d*)/$', 'workflow.views.case_views.resolve_case', name='resolve_case'),
    url(r'^workflow/forward_case/(?P<case_id>\d*)/$', 'workflow.views.case_views.forward_case', name='forward_case'),
    url(r'^workflow/revert_case/(?P<case_id>\d*)/$', 'workflow.views.case_views.revert_case', name='revert_case'),

    # verification related views
    url(r'^workflow/verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.verification', name='verfication'),
    url(r'^workflow/add_contact_action/$', 'workflow.views.verification_views.add_contact_action', name='add_contact_action'),
    url(r'^workflow/geocode_address/$', 'workflow.views.verification_views.geocode_address', name='geocode_address'),
    url(r'^workflow/resolve_verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.resolve_verification', name='resolve_verification'),
    url(r'^workflow/forward_verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.forward_verification', name='forward_verification'),
    url(r'^workflow/revert_verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.revert_verification', name='revert_verification'),

    # report related views
    url(r'^workflow/report/(?P<report_id>\d*)/$', 'workflow.views.report_views.report', name='report'),
    url(r'^workflow/reports/$', 'workflow.views.report_views.reports', name='reports'),
    url(r'^workflow/add_report/$', 'workflow.views.report_views.add_report', name='add_report'),
    url(r'^workflow/resolve_report/(?P<report_id>\d*)/$', 'workflow.views.report_views.resolve_report', name='resolve_report'),
    url(r'^workflow/forward_report/(?P<report_id>\d*)/$', 'workflow.views.report_views.forward_report', name='forward_report'),
    url(r'^workflow/verify_report/(?P<verification_id>\d*)/$', 'workflow.views.report_views.verify_report', name='verify_report'),

    # property related views
    url(r'^workflow/property/$', 'workflow.views.property_views.property', name='property'),
    url(r'^workflow/properties/$', 'workflow.views.property_views.properties', name='properties'),

    # landing, auth, and metircs page views
    url(r'^workflow/$', 'workflow.views.landing', name='landing'),
    url(r'^login/$', 'workflow.views.login_view', name='login_view'),
    url(r'^get_notifications/$', 'workflow.views.get_notifications', name='get_notifications'),
    url(r'^mark_notifications_seen/$', 'workflow.views.mark_notifications_seen', name='mark_notifications_seen'),
    url(r'^logout/$', 'workflow.views.logout_view', name='logout_view'),
    url(r'^metrics/$', 'workflow.views.metrics', name='metrics'),
)
