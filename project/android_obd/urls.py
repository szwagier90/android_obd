from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from android_obd.forms import MyAuthenticationForm
from android_obd.views import ProfileDetail


urlpatterns = patterns('android_obd.views',
	url(r'^$', 'index', name='index'),
	url(r'^register/$', 'register', name='register'),
	url(r'^route/$', 'route', name='route'),
	url(r'^profiles/$', 'profiles', name='profiles'),
	url(r'^register/$', 'index', name='more_recent'),
	url(r'^register/$', 'index', name='more_added'),
	url(r'^register/$', 'index', name='more_longest'),
	url(r'^register/$', 'index', name='more_fuel'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^accounts/login/$', 'login', {'template_name': 'android_obd/login.html', 'authentication_form': MyAuthenticationForm}, name='login'),
	url(r'^accounts/logout/$', 'logout', {'next_page': '/', 'template_name': 'android_obd/home.html'}, name='logout'),
)

urlpatterns += patterns('',
	url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(ProfileDetail.as_view(slug_field='username')), name='profile'),
)
