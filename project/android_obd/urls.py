from django.conf.urls import patterns, url
from android_obd.forms import MyAuthenticationForm


urlpatterns = patterns('android_obd.views',
	url(r'^$', 'index', name='index'),
	url(r'^register/$', 'register', name='register'),
	url(r'^route/$', 'route', name='route'),
	url(r'^register/$', 'index', name='more_recent'),
	url(r'^register/$', 'index', name='more_added'),
	url(r'^register/$', 'index', name='more_longest'),
	url(r'^register/$', 'index', name='more_fuel'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^login/$', 'login', {'template_name': 'android_obd/login.html', 'authentication_form': MyAuthenticationForm}, name='login'),
	url(r'^logout/$', 'logout', {'next_page': '/', 'template_name': 'android_obd/home.html'}, name='logout'),
)
