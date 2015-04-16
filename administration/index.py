import webapp2 as webapp

from administration.navbar import *
from administration.menu import *
from administration.link import *
from administration.admin_index import *
from administration.administrator import *
from authentification import *

app = webapp.WSGIApplication([
                ('/admin', AdminPage),
                ('/admin/', AdminPage),
                ('/admin/administrators', AdministratorsPage),
                (r'/admin/administrators/(.+)', AdministratorsPage),
                (r'/admin/menus/(.+)/reorder', LinksReorderTask),
                (r'/admin/menus/(.+)/links/', LinksPage),
                (r'/admin/menus/(.+)/links/(.+)', LinkPage),
                (r'/admin/menus/(.+)', MenuPage),
                ('/admin/menus/', MenusPage),
                ('/admin/navbars/', NavbarsPage),
                (r'/admin/navbars/(.+)/instructions', NavbarInstructionsPage),
                (r'/admin/navbars/(.+)', NavbarPage)
              ], debug=True)
