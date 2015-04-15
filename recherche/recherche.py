# Templates reference:
# http://www.djangoproject.com/documentation/0.96/templates/

import os
from google.appengine.ext.webapp import template

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


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

application = webapp.WSGIApplication(
                                     [('/', SearchHome)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
