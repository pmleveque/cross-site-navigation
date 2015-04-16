import webapp2 as webapp

from google.appengine.ext import db
from google.appengine.ext import ndb
import os
from google.appengine.ext.webapp import template
import pickle
import logging


class Menu(db.Model):
    name = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    # special_kind sert a identifier les menus qui servent
    #  a composer les menus speciaux (ressources, dioceses...)
    special_kind = db.StringProperty()
    author = db.UserProperty()
    shared = db.BooleanProperty()


class Link(db.Model):
    name = db.StringProperty(required=True)
    menu = db.ReferenceProperty(Menu)
    date = db.DateTimeProperty(auto_now_add=True)
    url = db.LinkProperty()
    order = db.IntegerProperty(required=True)


class Navbar(db.Model):
    # TODO: should be lowercase (will be the script filename)
    code = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    first_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_first_set")
    second_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_second_set")
    third_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_third_set")
    fourth_menu = db.ReferenceProperty(
        Menu, collection_name="navbar_fourth_set")
    settings = db.StringListProperty()
    # cse: custom search engine
    cse_unique_id = db.StringProperty()


class MenuNDB(ndb.Model):
    name = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    # use pickle.dumps() or .loads()
    links = ndb.PickleProperty()
    # special_kind sert a identifier les menus qui servent
    #  a composer les menus speciaux (ressources, dioceses...)
    special_kind = ndb.StringProperty()
    author = ndb.UserProperty()
    shared = ndb.BooleanProperty()


class NavbarNDB(ndb.Model):
    # TODO: should be lowercase (will be the script filename)
    code = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    author = ndb.UserProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    menus = ndb.StructuredProperty(MenuNDB, repeated=True)
    settings = db.StringListProperty()
    # cse: custom search engine
    cse_unique_id = db.StringProperty()


class Administrator(db.Model):
    user = db.UserProperty()
    admin = db.BooleanProperty(default=False)


class AdminPage(webapp.RequestHandler):

    def get(self):
        # L'option admin permet de voire toutes les barres
        # de navigation et tous les menus de tous les contributeurs

        menu1 = MenuNDB(
            name="test", links=pickle.dumps(Link.all())
        ).put()

        logging.debug("value of my var is %s", str(menu1))

        path = os.path.join(
            os.path.dirname(__file__),
            'admin2.html'
        )
        self.response.out.write(
            template.render(
                path,
                {'menu1': menu1,
                 'menus': Menu.all(),
                 'navbars': Navbar.all()
                 }
            )
        )

app = webapp.WSGIApplication([
    ('.*', AdminPage),
], debug=True)
