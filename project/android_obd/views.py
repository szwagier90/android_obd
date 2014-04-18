from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

def index(request):
	return render(request, 'android_obd/home.html', {})

def route(request):
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
	
	return render(request, 'android_obd/route.html', {"wsp":json_list})
