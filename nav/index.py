from models import MenuNDB, NavbarNDB, AdministratorNDB, MenuLinkNDB

import os
from google.appengine.ext.webapp import template

import webapp2 as webapp

class ShowMenus(webapp.RequestHandler):
    def get(self):
        navbar = NavbarNDB.query().fetch(1)[0]

        html_template_path = os.path.join(os.path.dirname(__file__), 'nav.html')

        html_template_values = {'navbar': navbar}

        self.response.out.write(template.render(html_template_path, html_template_values))


app = webapp.WSGIApplication(
                                     [('/nav/', ShowMenus)],
                                     debug=True)
