import webapp2
import facebook
import jinja2
import os
import urllib
from django.utils import simplejson as json

from models import *
from managers import *
from deezerExtractor import *
from facebookExtractor import *
from youtubeExtractor import *

PAGES_FOLDER = "pages/"
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
facebookExtractor = FacebookExtractor()

class BaseHandler(webapp2.RequestHandler):
	"""Provides access to the active Facebook user in self.current_user

	The property is lazy-loaded on first access, using the cookie saved
	by the Facebook JavaScript SDK to determine the user ID of the active
	user. See http://developers.facebook.com/docs/authentication/ for
	more information.
	"""
	@property
	def graph(self):
		return facebookExtractor.getGraph(self.request.cookies)

	@property
	def current_user(self):
		if not hasattr(self, "_current_user"):
			self._current_user = None
			cookie = facebookExtractor.getCurrentUserCookie(self.request.cookies)
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

	def returnJson(self, data):
		return self.response.out.write(json.dumps(data))

class MainPage(BaseHandler):
	def get(self):
		template_values = {
			'user': self.current_user
		}
		template = jinja.get_template(PAGES_FOLDER + 'index.html')
		self.response.out.write(template.render(template_values))

class UserHandler(BaseHandler):
	def get(self, param):
		if not self.current_user:
			return self.returnJson({"status": "ERROR"})

		ids = None
		if param: ids = param.split(",")
		else: ids = [self.current_user.facebookId]			

		userManager = UserManager()
		users = [u.toDict() for u in userManager.getUsers(ids)]
		status = "OK" if len(users) > 0 else "ERROR"
		jsonData = {"status": status, "data": users}
		return self.returnJson(jsonData)

class TrackHandler(BaseHandler):
	def get(self, criteria, param):
		ids = None
		if param:
			ids = param.split(",")

		jsonData = {"status": "ERROR"}
		if criteria == "artistId":
			trackManager = TrackManager()
			artistManager = ArtistManager()
			deezerExtractor = DeezerExtractor()
			youtubeExtractor = YouTubeExtractor()
			artists = artistManager.getArtists(ids)
			data = []
			for artist in artists:
				if artist.needsUpdate():
					tracks = deezerExtractor.getTracks(artist.toDict())
					tracksDict = []
					for t in tracks:
						video = youtubeExtractor.getVideo(artist.name, t["title"])
						tDict =  {
							"id": t["id"],
							"name": t["title"],
							"deezerUrl": t["link"],
							"videoUrl": video["url"]
						}
						try: tDict["deezerRank"] = t["rank"]
						except KeyError: pass
						try: tDict["previewUrl"] = t["preview"]
						except KeyError: pass
						tracksDict.append(tDict)
						
					tracks = trackManager.addTracks(tracksDict)
					artistManager.addTracks(artist, tracks)
				else:
					tracks = Track.get(artist.tracks)
				data.append({"artist": artist.name, "tracks": [t.toDict() for t in tracks]})
			jsonData = {"status": "OK", "data": data}
		elif criteria == "id":
			tracks = [t.toDict() for t in trackManager.getTracks(ids)]
			status = "OK" if len(tracks) > 0 else "ERROR"
			jsonData = {"status": status, "data": tracks}
		return self.returnJson(jsonData)

class TopArtistsHandler(BaseHandler):
	def get(self, numArtists):
		user = self.current_user
		if user:
			if numArtists: numArtists = int(numArtists)
			else: numArtists = 5

			topArtists = facebookExtractor.getTopFriendsMusic(numArtists, self.request.cookies)
			artistManager = ArtistManager()
			userManager = UserManager()
			deezerExtractor = DeezerExtractor()
			artists = []
			for artist in topArtists:
				artist = deezerExtractor.getArtist(artist["artist"])
				try: link = artist["link"]
				except KeyError: link = None
				try: picture = artist["picture"]
				except KeyError: picture = None
				artists.append({
					"id": artist["id"],
					"name": artist["name"],
					"deezerUrl": link,
					"pictureUrl": picture
				})
			artists = artistManager.addArtists(artists)
			user = userManager.addArtists(user, artists).toDict()
			jsonData = {"status": "OK", "data": user["topArtists"], "lastUpdated": user["lastUpdated"]}
			return self.returnJson(jsonData)
		else:
			return self.returnJson({"status": "ERROR"})


app = webapp2.WSGIApplication([
								('/', MainPage),
								('/user(?:/([^/]+)?)?', UserHandler),
								('/track/([^/]+)(?:/([^/]+)?)?', TrackHandler),
								('/topArtists(?:/([^/]+)?)?', TopArtistsHandler)
							],
							debug=True)
