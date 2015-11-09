from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # case related views
    url(r'^workflow/case/(?P<case_id>\d*)/$', 'workflow.views.case_views.case', name='case'),
    url(r'^workflow/cases/$', 'workflow.views.case_views.cases', name='cases'),
    url(r'^workflow/cases_data/$', 'workflow.views.case_views.cases_data', name='cases_data'),
    url(r'^workflow/add_case_assignee/$', 'workflow.views.case_views.add_case_assignee', name='add_case_assignee'),
    url(r'^workflow/remove_case_assignee/$', 'workflow.views.case_views.remove_case_assignee', name='remove_case_assignee'),

    # verification related views
    url(r'^workflow/verification/(?P<verification_id>\d*)/$', 'workflow.views.verification_views.verification', name='verfication'),
    url(r'^workflow/add_contact_action/$', 'workflow.views.verification_views.add_contact_action', name='add_contact_action'),

    # report related views
    url(r'^workflow/report/(?P<report_id>\d*)/$', 'workflow.views.report_views.report', name='report'),
    url(r'^workflow/reports/$', 'workflow.views.report_views.reports', name='reports'),
    url(r'^workflow/reports_data/$', 'workflow.views.report_views.reports_data', name='reports_data'),
    url(r'^workflow/add_report/$', 'workflow.views.report_views.add_report', name='add_report'),
    url(r'^workflow/resolve_report/(?P<report_id>\d*)/$', 'workflow.views.report_views.resolve_report', name='resolve_report'),

    # property related views
    # TODO: eventually expose by id
    # url(r'^workflow/property/(?P<property_id>\d*)/$', 'workflow.views.property_views.property', name='property'),
    url(r'^workflow/property/$', 'workflow.views.property_views.property', name='property'),
    url(r'^workflow/properties/$', 'workflow.views.property_views.properties', name='properties'),
)
