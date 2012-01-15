import webapp2
import facebook
import jinja2
import os
import urllib
from django.utils import simplejson as json

from models import *
from managers import *

PAGES_FOLDER = "pages/"
FB_APP_ID = '173535979414436'
FB_APP_SECRET = '7eef3a773b0a2da0eaedd3949d01ce89'
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
#facebookApi = facebook.Facebook(FB_API_KEY, FB_SECRET_KEY)

class BaseHandler(webapp2.RequestHandler):
	"""Provides access to the active Facebook user in self.current_user

	The property is lazy-loaded on first access, using the cookie saved
	by the Facebook JavaScript SDK to determine the user ID of the active
	user. See http://developers.facebook.com/docs/authentication/ for
	more information.
	"""
	@property
	def current_user(self):
		if not hasattr(self, "_current_user"):
			self._current_user = None
			cookie = facebook.get_user_from_cookie(self.request.cookies, FB_APP_ID, FB_APP_SECRET)
			if cookie:
				# Store a local instance of the user data so we don't need
				# a round-trip to Facebook on every request
				user = User.get_by_key_name(cookie["uid"])
				if not user:
					#graph = facebook.GraphAPI(cookie["access_token"])
					#profile = graph.get_object("me")
					#user = User(key_name=str(profile["id"]),
					#			id=str(profile["id"]),
					#			name=profile["name"],
					#			profile_url=profile["link"],
					#			access_token=cookie["access_token"])
					userManager = UserManager()
					uData = [{"id": cookie["uid"], "name": "unknown", "access_token": cookie["access_token"]}]
					user = userManager.addUsers(uData)[0]
				elif user.access_token != cookie["access_token"]:
					user.access_token = cookie["access_token"]
					user.put()
				self._current_user = user
		return self._current_user

class MainPage(BaseHandler):
	def get(self):
		template_values = {
			'user': self.current_user
		}
		template = jinja.get_template(PAGES_FOLDER + 'index.html')
		self.response.out.write(template.render(template_values))

class ApiRequestHandler(BaseHandler):
	def __init__(self, request, response, manager):
		webapp2.RequestHandler.__init__(self, request, response)
		self.manager = manager

	def get(self, param):
		return self.returnJson({"status": "ERROR"})

	def post(self, param):
		return self.returnJson({"status": "ERROR"})

	def returnJson(self, data):
		return self.response.out.write(json.dumps(data))

class UserHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, UserManager())
		
	def get(self, param):
		ids = None
		if param:
			ids = param.split(",")

		jsonData = {"data": self.manager.getUsers(ids)}
		return self.returnJson(jsonData)

	def post(self, param):
		retData = {}
		jsonStr = self.request.get("json")
		data = json.loads(jsonStr)

		users = self.manager.addUsers(data["data"])
		if users:
			return self.returnJson({"status": "OK"})
		else:
			return self.returnJson({"status": "ERROR"})
			
class ArtistHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, ArtistManager())

	def get(self, param):
		ids = None
		if param:
			ids = param.split(",")

		jsonData = {"data": self.manager.getArtists(ids)}
		return self.returnJson(jsonData)

	def post(self, param):
		retData = {}
		#try:
		jsonStr = self.request.get("json")
		data = json.loads(jsonStr)

		artists = self.manager.addArtists(data["data"])
		if artists:
			return self.returnJson({"status": "OK"})
		else:
			return self.returnJson({"status": "ERROR"})
		#except:
		#	return self.returnJson({"status": "ERROR"})

class TrackHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, TrackManager())

	def get(self, param):
		#param = urllib.unquote(urllib.unquote(param))
		jsonData = {"data": self.manager.getTracks()}
		return self.returnJson(jsonData)

	def post(self, param):
		#param = urllib.unquote(urllib.unquote(param))
		retData = {}
		try:
			jsonStr = self.request.get("json")
			data = json.loads(jsonStr)

			tracks = self.manager.addTracks(data["data"])
			if tracks:
				return self.returnJson({"status": "OK"})
			else:
				return self.returnJson({"status": "ERROR"})
		except:
			return self.returnJson({"status": "ERROR"})

class TopArtistsHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, None)

	def get(self):
		user = self.current_user
		if user:
			allArtists = {}
			for friend in user.friends:
				for artist in friend.preferedArtists:
					try:
						allArtists[artist] += 1
					except KeyError:
						allArtists[artist] = 0

			artistValues = allArtists.items()
			artistValues.sort()
			topArtists = {}
			for key, value in artistValues[:5]:
				topArtists['artist']= key
				topArtists['friends'] = value

			jsonData = {"status": "OK", "data": topArtists}
			return self.returnJson(jsonData)
		else:
			return self.returnJson({"status": "ERROR"})

app = webapp2.WSGIApplication([
								('/', MainPage),
								('/user(?:/([^/]+)?)?', UserHandler),
								('/artist(?:/([^/]+)?)?', ArtistHandler),
								('/track(?:/([^/]+)?)?', TrackHandler),
								('/topArtists', TopArtistsHandler),
							],
							debug=True)
