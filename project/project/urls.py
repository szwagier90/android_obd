from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^android_obd/', include('android_obd.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
