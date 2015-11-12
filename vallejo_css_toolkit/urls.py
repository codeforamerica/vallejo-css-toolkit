from django.contrib import admin
from django.conf.urls import patterns, include, url

from data_load.urls import urlpatterns as data_load_urlpatterns
from workflow.urls import urlpatterns as workflow_urlpatterns
from intake.urls import urlpatterns as intake_urlpatterns

urlpatterns = patterns(
    '',
    # admin url
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += data_load_urlpatterns
urlpatterns += workflow_urlpatterns
urlpatterns += intake_urlpatterns
