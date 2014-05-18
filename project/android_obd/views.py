# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from android_obd.forms import MyUserCreationForm, UserNameChangeForm
from android_obd.models import Record
from django.views.generic import DetailView

from django.utils import simplejson

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from face import *



class ProfileDetail(DetailView):
	model = User
	template_name = 'android_obd/profile_detail_view.html'

def index(request):
	most_added = User.objects.annotate(records_count = Count('record')).order_by('-records_count')[:10]
	last_added = Record.objects.all().order_by('-id')[:5]
	
	if request.GET.get("code") != None:
		code2token(request.GET.get("code"))

	return render(request, 'android_obd/home.html',{'most_added': most_added,'last_added':last_added, 'tags':tags})

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

def face(request):

	FACEBOOK_APP_ID     = '1480924338806342'
	FACEBOOK_APP_SECRET = 'ac8ab41856683368a125f6d7d1a186ee'
	
	app_id = FACEBOOK_APP_ID
	redirect_uri = 'http://156.17.234.28:8888/'

	www="https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s"%(app_id, redirect_uri)
	
	return HttpResponseRedirect(www)

def profile_edit(request):
	info = []
	
	current_user = User.objects.get(username=request.user)

	if request.method == 'POST':
		form = UserNameChangeForm(request.POST)
		if form.is_valid():
			user = authenticate(username=request.user, password=form.cleaned_data['password'])
			if user is None:
				info.append('Podane niewłaściwe hasło')
			else:
				current_user.first_name = form.cleaned_data['first_name']
				current_user.last_name = form.cleaned_data['last_name']
				current_user.save()
				return HttpResponseRedirect(reverse('profile', kwargs={'slug': request.user}))
		else:
			return render(request, 'android_obd/profile_edit.html', 
				{'form': form})

	form = UserNameChangeForm(initial={'first_name': current_user.first_name, 'last_name': current_user.last_name})
	return render(request, 'android_obd/profile_edit.html', 
		{'form': form})

@login_required
def all_routes(request):
        records_list = Record.objects.filter(user=request.user)
        paginator = Paginator(records_list, 1) # Show 1 contacts per page

        page = request.GET.get('page')
        try:
           records = paginator.page(page)
        except PageNotAnInteger:
           records = paginator.page(1)
        except EmptyPage:
           records = paginator.page(paginator.num_pages)

        return render(request,'android_obd/all_routes.html',{"records": records})


def route(request, id=5):

	lista =  [
        {'X':37.60,'Y':-121.44,'spalanie':0,'predkosc':0},
        {'X':37.7699298,'Y':-118.4469157,'spalanie': 4,'predkosc':78},
        {'X':36.7699298,'Y':-120.4469157,'spalanie': 7,'predkosc':56},
        {'X':38.7699298,'Y':-120.4469157,'spalanie': 8,'predkosc':30},
        {'X':37.7699298,'Y':-122.4469157,'spalanie':12},
        {'X':40.7699298,'Y':-122.4469157,'spalanie':21,'predkosc':185}
        ]

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

def tags(request, tag="brak"):
       
	tags = Record.objects.filter(tags__name=tag)
        return render(request, 'android_obd/tags.html',{"tags":tags,"name":tag})
