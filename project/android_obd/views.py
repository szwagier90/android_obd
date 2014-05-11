# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from android_obd.forms import MyUserCreationForm
from android_obd.models import Record
from django.views.generic import DetailView

from django.utils import simplejson

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProfileDetail(DetailView):
	model = User
	template_name = 'android_obd/profile_detail_view.html'

def index(request):
	return render(request, 'android_obd/home.html')

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password2']
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect(reverse('profile', kwargs={'slug': username}))
		else:
			return render(request, 'android_obd/register.html', 
				{'form': form})

	form = MyUserCreationForm()
	return render(request, 'android_obd/register.html', 
		{'form': form})

@login_required
def all_routes(request):
        records_list = Record.objects.filter(user=request.user)
        paginator = Paginator(records_list, 1) # Show 2 contacts per page

        page = request.GET.get('page')
        try:
           records = paginator.page(page)
        except PageNotAnInteger:
           # If page is not an integer, deliver first page.
           records = paginator.page(1)
        except EmptyPage:
           # If page is out of range (e.g. 9999), deliver last page of results.
           records = paginator.page(paginator.num_pages)

        return render(request,'android_obd/all_routes.html',{"records": records})


def route(request, id=5):
	#slownik = {"wsp": [['Y',-121.44],['X',37.78]]}
	#slownik = {"wsp": [['Y',-121.4],['X',37.7699298]]}

	lista =  [
        {'X':37.60,'Y':-121.44,'spalanie':0,'predkosc':0},
        {'X':37.7699298,'Y':-118.4469157,'spalanie': 4,'predkosc':78},
        {'X':36.7699298,'Y':-120.4469157,'spalanie': 7,'predkosc':56},
        {'X':38.7699298,'Y':-120.4469157,'spalanie': 8,'predkosc':30},
        {'X':37.7699298,'Y':-122.4469157,'spalanie':12},
        {'X':40.7699298,'Y':-122.4469157,'spalanie':21,'predkosc':185}
        ]

	#slownik = {"wsp":[-121.44, 37.77]}
	json_list = simplejson.dumps(lista)
	
	return render(request, 'android_obd/route.html', {"wsp":json_list,"my_id":id })

@login_required
def profiles(request):
	info = []
	username = request.POST.get('username', '')
	if username:
		try:
			user = User.objects.get(username=username)
			return HttpResponseRedirect(reverse('profile', kwargs={'slug': username}))
		except User.DoesNotExist:
			info.append('Taki użytkownik nie istnieje')

	recent_users_list = User.objects.order_by('-date_joined')[:10]
	return render(request, 'android_obd/profiles.html',
		{'recent_users_list': recent_users_list, 'info': info})
