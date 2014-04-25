from django.conf.urls import patterns, url


urlpatterns = patterns('android_obd.views',
	url(r'^$', 'index', name='index'),
	url(r'^register/$', 'register', name='register'),
	url(r'^login/$', 'login_view', name='login'),
	url(r'^route/$', 'route', name='route'),
	url(r'^register/$', 'index', name='more_recent'),
	url(r'^register/$', 'index', name='more_added'),
	url(r'^register/$', 'index', name='more_longest'),
	url(r'^register/$', 'index', name='more_fuel'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^logout/$', 'logout', {'template_name': 'android_obd/home.html'}, name='logout'),
)
