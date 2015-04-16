# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

import os
from google.appengine.ext.webapp import template

import webapp2 as webapp


class SearchHome(webapp.RequestHandler):
    def get(self):
        sites = self.request.get('sites')
        q = self.request.get('q')

        html_template_path = os.path.join(
            os.path.dirname(__file__), 'recherche.html')

        html_template_values = {
            'sites': sites,
            'q': q
        }

        self.response.out.write(
            template.render(html_template_path, html_template_values))

app = webapp.WSGIApplication(
                                     [('/', SearchHome)],
                                     debug=True)
