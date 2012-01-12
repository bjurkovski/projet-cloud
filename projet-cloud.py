import webapp2
import facebook
import jinja2
import os
from django.utils import simplejson as json

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

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
