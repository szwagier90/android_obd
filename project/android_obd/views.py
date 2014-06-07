# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from android_obd.forms import MyUserCreationForm, UserNameChangeForm
from android_obd.models import Record, Tag, Measurement
from django.views.generic import DetailView

from django.middleware import csrf
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from face import face_auth, generator
from django.conf import settings

import random
import json
import re

import sys

from django.core import serializers


class ProfileDetail(DetailView):
	model = User
	template_name = 'android_obd/profile_detail_view.html'

def index(request):
	most_added = User.objects.annotate(records_count = Count('record')).exclude(records_count=0).order_by('-records_count')[:5]
	last_added = Record.objects.all().order_by('-id')[:5]
	longest_distance = User.objects.annotate(total_distance=Sum('record__distance')).exclude(total_distance=None).order_by('-total_distance')[:5]
	smallest_fuel_consumption = User.objects.annotate(total_fuel_consumption=Sum('record__fuel_consumption')).exclude(total_fuel_consumption=None).order_by('-total_fuel_consumption')[:5]
	return render(request, 'android_obd/home.html', 
		{'most_added': most_added,
		 'last_added': last_added,
		 'longest_distance': longest_distance,
		 'smallest_fuel_consumption': smallest_fuel_consumption})

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
	scope = ['email']
	redirect_uri = settings.DOMAIN+'/face/auth'
	
	#face_auth().publish("wiadomosc",requests.session['token']
	
	#wymiana code na token i rejestracja/logowanie w app
	if request.GET.get("code") != None:
		token, me = face_auth().code2token(request.GET.get("code"))
		try:
			User.objects.get(email=me['email'])
		except:
			u=User(username=me['email'], email=me['email'], password=generator().gen)
			u.save()
		
		user = User.objects.get(email=me['email'])
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		request.session["token"]=token
		login(request, user)
		return HttpResponseRedirect(reverse('profile', kwargs={'slug': user.username}))

	#przekierowanie na logowanie do FB
	www = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=%s"%(settings.FACEBOOK_APP_ID, redirect_uri,scope)
	
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
        paginator = Paginator(records_list, 10) # Show 10 contacts per page

        page = request.GET.get('page')
        try:
           records = paginator.page(page)
        except PageNotAnInteger:
           records = paginator.page(1)
        except EmptyPage:
           records = paginator.page(paginator.num_pages)

        return render(request,'android_obd/all_routes.html',{"records": records})


def route(request, id=5):

	
	if request.method == 'POST':
		record = Record.objects.get(id=id)

		if request.POST.get("False"):
			public = False
			record.public = public
		if request.POST.get("True"):
			public = True
			record.public = public
		if request.POST.get("link"):
			pattern = "https?://www\.youtube\.com/watch\?v=([\w+\-]+)"
			result = re.match(pattern, request.POST.get("link"))
			if result==None:
				return HttpResponse('Nieprawidlowe format adresu dla filmu')
			else:
				link = result.group(1) #zapisujemy to do bazy
				print link
				record.video_link = link
		
		record.save()

	def f(x):
		if x != None:
			return float(str(x))
		else:
			return 'brak danych'
	
	def wsp(x):
        	if x != None:
        		return float(str(x))
        	else:
        		return 0.0 

	lista = []
	count = 0
	pomiar = Measurement.objects.filter(record__id=id)

	for x in pomiar:
		s = {}
		s['id']=count
		s['time']=int(str(x.timestamp))
		s['AccX'] = f(x.AccX)
		s['AccY'] = f(x.AccY)
		s['AccZ'] = f(x.AccZ)
		s['speed']=f(x.speed)
		s['rotation']=f(x.rotation)
		s['Z']=f(x.altitude)
		s['X']=wsp(x.latitude)
		s['Y']=wsp(x.longitude)
		lista.append(s)
		count+=1

	record = Record.objects.get(id=id)

	return render(request, 'android_obd/route.html', {"wsp":lista, "record":record})

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

def more(request, type, page=1):
	titles = {
		'recent': 'Ostatnio dodane przejazdy',
		'added': 'Najwięcej dodanych przejazdów',
		'longest': 'Największy dystans',
		'fuel': 'Najmniejsze spalanie'
	}

	more = {}
	more['type'] = type
	more['title'] = titles.get(type)
	if more['title']:
		if type == 'recent':
			more['columns'] = [{'name': 'Nr', 'span': 1}, {'name': 'Użytkownik', 'span': 2}, {'name': 'Link Video', 'span': 5}, {'name': 'Tagi', 'span': 3}, {'name': 'Szczegóły', 'span': 1}]
			records_list = Record.objects.all().order_by('-id')
			record_paginator = Paginator(records_list, 10)
			try:
				more['records'] = record_paginator.page(page)
			except PageNotAnInteger:
				more['records'] = record_paginator.page(1)
			except EmptyPage:
				more['records'] = record_paginator.page(record_paginator.num_pages)
			return render(request, 'android_obd/more_recent.html', {'more': more})
		elif type == 'added':
			more['columns'] = [{'name': 'Użytkownik', 'span': 3}, {'name': 'Przejazdów', 'span': 1}]
			records_list = User.objects.annotate(record_stat = Count('record')).order_by('-record_stat')
		elif type == 'longest':
			more['columns'] = [{'name': 'Użytkownik', 'span': 3}, {'name': 'Łączny dystans', 'span': 1}]
			records_list = User.objects.annotate(record_stat=Sum('record__distance')).exclude(record_stat=None).order_by('-record_stat')
		elif type == 'fuel':
			more['columns'] = [{'name': 'Użytkownik', 'span': 3}, {'name': 'Najmniejsze spalanie', 'span': 1}]
			records_list = User.objects.annotate(record_stat=Sum('record__fuel_consumption')).exclude(record_stat=None).order_by('record_stat')
	else:
		return HttpResponseRedirect(reverse('index'))

	record_paginator = Paginator(records_list, 10)
	try:
		more['records'] = record_paginator.page(page)
	except PageNotAnInteger:
		more['records'] = record_paginator.page(1)
	except EmptyPage:
		more['records'] = record_paginator.page(record_paginator.num_pages)
	return render(request, 'android_obd/more.html',
		{'more': more})	

def android_test(request):
	return render(request, 'android_obd/android_auth_test.html')

def android_csrf(self):
	return HttpResponse(csrf.get_token(request))

def android_auth(request):
	if request.method == 'POST':
		json_login_data = request.POST.get('login')
		if json_login_data:
			print >>sys.stderr, 'LOGIN W POST'
			try:
				login_data = json.loads(json_login_data)
			except ValueError:
				print >>sys.stderr, 'JSON_error'
				return HttpResponse("JSON_error")
			else:
				print >>sys.stderr, 'JSON_LOGIN_ROZPAKOWANY'
				username = login_data.get('username')
				password = login_data.get('password')
				if username and password:
					print >>sys.stderr, 'KLUCZE ODNALEZIONE'
					user = authenticate(username=username, password=password)
					if user:
						print >>sys.stderr, 'UZYTKOWNIK ODNALEZIONY'
						return HttpResponse(user.id)
					else:
						print >>sys.stderr, 'LOGOWANIE NIEPOPRAWNE'
						return HttpResponse('-1')
				else:
					print >>sys.stderr, 'BRAK KLUCZY DO LOGOWANIA'
					return HttpResponse('AUTHENTICATION_JSON_INCOMPLETE')
		return HttpResponse('LOGIN_KEY_NOT_FOUND')
	else:
		return HttpResponse('NOT_POST')

def android_upload(request):
	if request.method != 'POST':
		return HttpResponse('NOT_POST')
	print >>sys.stderr, 'POST'
	
	record_json = request.POST.get('record')
	if not record_json:
		return HttpResponse('NO_RECORD_IN_POST')
	print >>sys.stderr, 'RECORD IN POST'

	record_data = json.loads(record_json)
	if not record_data:
		return HttpResponse('INVALID_RECORD_JSON')
	print >>sys.stderr, 'RECORD JSON VALID'

	username = record_data.get('username')
	if not username:
		return HttpResponse('NO_USERNAME_IN_RECORD_JSON')
	print >>sys.stderr, 'USERNAME IN RECORD JSON'

	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return HttpResponse('USER_DOES_NOT_EXIST')
	else:
		print >>sys.stderr, 'USERNAME "%s" IN RECORD JSON' % user

	distance = record_data.get('distance')
	if not distance:
		return HttpResponse('NO_DISTANCE_IN_RECORD_JSON')
	print >>sys.stderr, 'DISTANCE "%d" IN RECORD JSON' % distance

	public = record_data.get('public', False)
	print >>sys.stderr, 'PUBLIC "%s" IN RECORD JSON' % public

	measurements_json = request.POST.get('measurements')
	if not measurements_json:
		return HttpResponse('NO_MEASUREMENTS_IN_POST')
	print >>sys.stderr, 'MEASUREMENTS IN POST'

	measurements = json.loads(measurements_json)
	if not measurements:
		return HttpResponse('INVALID_MEASUREMENT_JSON')
	print >>sys.stderr, 'MEASUREMENT JSON VALID'
	
	r = Record(user=user, distance=distance, fuel_consumption=0, public=public)
	r.save()
	print >>sys.stderr, r

	tags = record_data.get('tags')
	if tags:
		print >>sys.stderr, 'TAGS "%s" IN RECORD JSON' % tags
		for tag in tags:
			t = Tag.objects.get_or_create(name=tag)
			r.tags.add(t[0])
		r.save()
		print >>sys.stderr, r
	else:
		print >>sys.stderr, 'NO TAGS IN RECORD' % public

#	for measurement in measurements:
#		print >>sys.stderr, "timestamp: %d" % measurement['timestamp']
#		print >>sys.stderr, measurement['measurements']
#		for key, value in measurement['measurements'].iteritems():
#			print >>sys.stderr, "%s: %s" % (key, value)
#		print >>sys.stderr, "\n"
	return HttpResponse("%s" % (measurements[0]))
