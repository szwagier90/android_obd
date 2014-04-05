from django.conf.urls import patterns, url
from android_obd import views

urlpatterns = patterns('',
	url(r'', views.index),
)