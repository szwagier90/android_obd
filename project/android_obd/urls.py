from django.conf.urls import patterns, url
from android_obd import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^route/$', views.route, name='route'),
	url(r'^register/$', views.index, name='more_recent'),
	url(r'^register/$', views.index, name='more_added'),
	url(r'^register/$', views.index, name='more_longest'),
	url(r'^register/$', views.index, name='more_fuel'),
)