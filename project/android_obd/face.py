FACEBOOK_APP_ID     = '1480924338806342'
FACEBOOK_APP_SECRET = 'ac8ab41856683368a125f6d7d1a186ee'
	
import urllib
import cgi
from open_facebook.api import OpenFacebook

def code2token(code):
	
	redirect_uri = 'http://156.17.234.28:8888/'
	www = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s"%(FACEBOOK_APP_ID, redirect_uri, FACEBOOK_APP_SECRET, code)
	response = cgi.parse_qs(urllib.urlopen(www).read())
        access_token = response['access_token'][-1]
	expires = response['expires'][-1]
	print response
	print access_token
	print expires

	graph = OpenFacebook(access_token)
	print graph.get('me')
	#graph.set('me/feed', message='facebook test')
	print graph.get('me/permissions') 
