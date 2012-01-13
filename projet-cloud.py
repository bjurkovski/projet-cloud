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
					user = User(key_name=str(cookie["uid"]),
								id=str(cookie["uid"]),
								name="unknown",
								profile_url="unknown",
								access_token=cookie["access_token"])
					user.put()
				elif user.access_token != cookie["access_token"]:
					user.access_token = cookie["access_token"]
					user.put()
				self._current_user = user
		return self._current_user

class MainPage(BaseHandler):
	def get(self):
		template_values = {
			'param': 'This is a parameter to the page renderer!',
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
		param = urllib.unquote(urllib.unquote(param))
		retData = {}
		try:
			jsonStr = self.request.get("json")
			data = json.loads(jsonStr)

			retData = self.manager.addArtists(data["data"])
		except:
			retData = {"status": "ERROR"}

		return self.returnJson(retData)

class TrackHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, TrackManager())

	def get(self, param):
		param = urllib.unquote(urllib.unquote(param))
		jsonData = {"data": self.manager.getTracks()}
		return self.returnJson(jsonData)

	def post(self, param):
		param = urllib.unquote(urllib.unquote(param))
		retData = {}
		try:
			jsonStr = self.request.get("json")
			data = json.loads(jsonStr)

			retData = self.manager.addTracks(data["data"])
		except:
			retData = {"status": "ERROR"}

		return self.returnJson(retData)

app = webapp2.WSGIApplication([
								('/', MainPage),
								('/artist(?:/([^/]+)?)?', ArtistHandler),
								('/track(?:/([^/]+)?)?', TrackHandler),
							],
							debug=True)
