import webapp2
import jinja2
import os

PAGES_FOLDER = "pages/"
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'param': 'This is a parameter to the page renderer!'
		}
		template = jinja.get_template(PAGES_FOLDER + 'index.html')
		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
