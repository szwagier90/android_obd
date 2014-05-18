from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from android_obd.forms import MyAuthenticationForm
from android_obd.views import ProfileDetail


urlpatterns = patterns('android_obd.views',
	url(r'^$', 'index', name='index'),
	url(r'^register/$', 'register', name='register'),
	url(r'^profile_edit/$', 'profile_edit', name='profile_edit'),
	url(r'^profiles/$', 'profiles', name='profiles'),
	url(r'^route/(?P<id>[0-9]+)/$', 'route', name='route'),
	url(r'^register/$', 'index', name='more_recent'),
	url(r'^register/$', 'index', name='more_added'),
	url(r'^register/$', 'index', name='more_longest'),
	url(r'^register/$', 'index', name='more_fuel'),
	url(r'^routes/$', 'all_routes', name='routes'),
	url(r'^tags/(?P<tag>.+)/$', 'tags', name='tags'),
	url(r'^face/auth/$','face',name='facebook'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^accounts/login/$', 'login', {'template_name': 'android_obd/login.html', 'authentication_form': MyAuthenticationForm}, name='login'),
	url(r'^accounts/logout/$', 'logout', {'next_page': '/', 'template_name': 'android_obd/home.html'}, name='logout'),
)

urlpatterns += patterns('',
	url(r'^profile/(?P<slug>[\w.@+-]+)/$', login_required(ProfileDetail.as_view(slug_field='username')), name='profile'),
)
