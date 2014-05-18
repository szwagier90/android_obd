#FACEBOOK_APP_ID     = '1480924338806342'
#FACEBOOK_APP_SECRET = 'ac8ab41856683368a125f6d7d1a186ee'
	
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import cgi
from open_facebook.api import OpenFacebook
from django.conf import settings

class face_auth:
	redirect_uri = settings.DOMAIN+'/face/auth'
	
	def code2token(self, code):
		me = {}
		www = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s"%(settings.FACEBOOK_APP_ID, self.redirect_uri, settings.FACEBOOK_APP_SECRET, code)
		response = cgi.parse_qs(urllib.urlopen(www).read())
		access_token = response['access_token'][-1]
		expires = response['expires'][-1]
		#print response
		#print access_token
		#print expires
		graph = OpenFacebook(access_token)
		me = dict(graph.get('me'))
		print me
		return access_token, me

	def publish(self, text):
	
		
		graph = OpenFacebook(access_token)
		try:
			graph.set('me/feed',message=text)
		except:
			www = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=publish_actions"%(settings.FACEBOOK_APP_ID,self.redirect_uri)
			return 'perm', www
			

	#	return www2
		
		#r2 = urllib.urlopen(www).read()
		#print r2
		#print graph.get('me')

		#graph.set('me/feed', message='facebook test22')
		#print graph.get('me/permissions')
	 
