from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

def index(request):
	return render(request, 'android_obd/home.html', {})

def route(request):
	#slownik = {"wsp": [['Y',-121.44],['X',37.78]]}
	#slownik = {"wsp": [['Y',-121.4],['X',37.7699298]]}
	
	lista =  [
		{'X':37.60,'Y':-121.44},{'X':37.7699298}
	]
	#slownik = {"wsp":[-121.44, 37.77]}
	json_list = simplejson.dumps(lista)
	
	return render(request, 'android_obd/route.html', {"wsp":json_list})
