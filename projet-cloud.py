import webapp2
import facebook
import jinja2
import os
import urllib
from django.utils import simplejson as json

from models import *
from managers import *

PAGES_FOLDER = "pages/"
FB_API_KEY = ''
FB_SECRET_KEY = ''
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
facebookApi = facebook.Facebook(FB_API_KEY, FB_SECRET_KEY)

class MainPage(webapp2.RequestHandler):
	def get(self):
		# json.dumps(data)
		# json.loads(self.request.get("json"))

		user = None
		if not facebookApi.check_connect_session(self.request):
			user = None

		try:
			users = facebookApi.users.getInfo([facebookApi.uid], ['uid', 'name'])
			user = users[0]
		except:
			pass

		template_values = {
			'param': 'This is a parameter to the page renderer!',
			'user': user
		}
		template = jinja.get_template(PAGES_FOLDER + 'index.html')
		self.response.out.write(template.render(template_values))

class ApiRequestHandler(webapp2.RequestHandler):
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
