from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^intake/welcome/$', 'intake.views.welcome', name='welcome'),
    url(r'^intake/handle-name/', 'intake.views.handle_name', name='handle_name'),
    url(r'^intake/handle-feedback-pref/', 'intake.views.handle_feedback_pref', name='handle_feedback_pref'),
    url(r'^intake/handle-feedback-number/', 'intake.views.handle_feedback_number', name='handle_feedback_number'),
    url(r'^intake/handle-problem-address/', 'intake.views.handle_problem_address', name='handle_problem_address'),
    url(r'^intake/handle-problem-description/', 'intake.views.handle_problem_description', name='handle_problem_description'),
)
