from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'android_obd/home.html', {})

def route(request):
	return render(request, 'android_obd/route.html', {})