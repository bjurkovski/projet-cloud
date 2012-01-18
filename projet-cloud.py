import webapp2
import facebook
import jinja2
import os
import urllib
from django.utils import simplejson as json

from models import *
from managers import *
from deezer import *
from facebookMediator import *

PAGES_FOLDER = "pages/"
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
facebookMediator = FacebookMediator()

class BaseHandler(webapp2.RequestHandler):
	"""Provides access to the active Facebook user in self.current_user

	The property is lazy-loaded on first access, using the cookie saved
	by the Facebook JavaScript SDK to determine the user ID of the active
	user. See http://developers.facebook.com/docs/authentication/ for
	more information.
	"""
	@property
	def graph(self):
		return facebookMediator.getGraph(self.request.cookies)

	@property
	def current_user(self):
		if not hasattr(self, "_current_user"):
			self._current_user = None
			cookie = facebookMediator.getCurrentUserCookie(self.request.cookies)
			if cookie:
				# Store a local instance of the user data so we don't need
				# a round-trip to Facebook on every request
				user = User.get_by_key_name(cookie["uid"])
				if not user:
					graph = facebook.GraphAPI(cookie["access_token"])
					profile = graph.get_object("me")
					#			profile_url=profile["link"],
					userManager = UserManager()
					uData = [{"id": profile["id"], "name": profile["name"], "access_token": cookie["access_token"]}]
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
		jsonStr = self.request.get("json")
		data = json.loads(jsonStr)
		if param == "update":
			return self.returnJson({"status": "OK"})
		else:
			retData = {}
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

class FacebookHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, None)

	def get(self):
#		code examples (might be useful in the future)
#		friendsJson = self.graph.get_connections("me", "friends")
#		music = self.graph.get_connections(friend["id"], "music")
#		requests[currentRequest].append({"method": "GET", "relative_url": friend["id"]+"/music"})
		deezerMediator = DeezerAPI()
		topArtists = facebookMediator.getTopFriendsMusic(5, self.request.cookies)
		for artist in topArtists:
			a = deezerMediator.getArtist(artist["artist"])
			allTracks = deezerMediator.getSongs(a)
			tracks = allTracks[:min(5, len(allTracks))]
			artist["tracks"] = tracks

		jsonData = {"data": topArtists}
		return self.returnJson(jsonData)

class DeezerSongHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, None)
		
	def get(self, query):
		return None

class DeezerArtistHandler(ApiRequestHandler):
	def __init__(self, request, response):
		ApiRequestHandler.__init__(self, request, response, None)
		
	def get(self, query):
		return None
		

app = webapp2.WSGIApplication([
								('/', MainPage),
								('/user(?:/([^/]+)?)?', UserHandler),
								('/artist(?:/([^/]+)?)?', ArtistHandler),
								('/track(?:/([^/]+)?)?', TrackHandler),
								('/topArtists', TopArtistsHandler),
								('/facebook', FacebookHandler),
								('/deezerSongs', DeezerSongHandler),
								('/deezerArtist', DeezerArtistHandler),
							],
							debug=True)
