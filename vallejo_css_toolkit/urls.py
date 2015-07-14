from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^intake/welcome/$', 'intake.views.welcome', name='welcome'),
    url(r'^intake/handle_name/', 'intake.views.handle_name', name='handle_name'),
    url(r'^intake/handle_feedback_pref/', 'intake.views.handle_feedback_pref', name='handle_feedback_pref'),
    url(r'^intake/handle_feedback_number/', 'intake.views.handle_feedback_number', name='handle_feedback_number'),
    url(r'^intake/handle_problem_address/', 'intake.views.handle_problem_address', name='handle_problem_address'),
)
